# C01KumitateOverlap — sibling overlap, kumitate `scripts/sources-check.mjs`

Seat: TameshiR18.C01KumitateOverlap. Date: 2026-10-20. Read-only on
`/home/vgpnk/Projects/shokunin/kumitate-shokunin`. No kumitate file was edited.
No `GIT_DIR` / `GIT_WORK_TREE` / `GIT_INDEX_FILE` / `GIT_COMMON_DIR` was set.
Git reads used `git --no-optional-locks -C` only. Scratch copies and selftests
lived under `/tmp/tameshi-r18w1-C01KumitateOverlap-Uecl8v` (cwd `/tmp` copy, not
the lane). No tool was installed.

Axes checked: whether the target file is moving, whether kumitate claims or
plans mutation testing of it, and whether a tameshi case on it absorbs
kumitate's domain under tameshi `PROVINCE.md` **Refuses**.

Round-17 §7 (`corpus/lessons/round-17-verifier-spotcheck.md:415-452`) routes
eight defects (R17-KNOW-EXIT through R17-INCIDENT). None names this file or
this overlap.

## 1. The file is not changing

Kumitate `HEAD` = `origin/master` = `1770305fae20826b39905a8251ddeca6b4957ac4`
(`master`, in sync). Single worktree: the lane checkout itself. No `.jj`
directory. `0acb7752d19058b953ebbeba253b1e35f6548de5` is an ancestor of `HEAD`
(`merge-base --is-ancestor`, exit 0). That commit is the file's last touch:

```text
git log -1 --format='%H %ci %s' 0acb7752d19058b953ebbeba253b1e35f6548de5
0acb7752d19058b953ebbeba253b1e35f6548de5 2026-10-19 20:44:37 -0300 round-34: fix SOURCES Markdown row parsing
```

Exit 0. Same command with `-- scripts/sources-check.mjs` lists that commit
first; the two parents of the file are `06757b0da6c790f823bf765aff366274dc5e1a5a`
(2026-10-19 20:30:44 -0300, `round-34: post-review fixes`) and
`1a8eed5aaa32043cf109dd28ceb5cd37ccd5555e` (2026-10-19 19:41:02 -0300,
`round-34: sources-registry gate …`).

History since the pin, this path, including `--all` and `--follow`: empty,
exit 0.

```text
git log --format='%H %ci %s' 0acb7752d19058b953ebbeba253b1e35f6548de5..HEAD -- scripts/sources-check.mjs
```

Working tree matches the pin:

| check | exit | result |
|---|---|---|
| `status --porcelain -- scripts/sources-check.mjs` | 0 | empty |
| `status --porcelain` (whole repo) | 0 | empty |
| `diff --exit-code -- scripts/sources-check.mjs` | 0 | no worktree diff |
| `diff --stat 0acb7752… HEAD -- scripts/sources-check.mjs` | 0 | empty |
| `rev-parse 0acb7752:scripts/sources-check.mjs` and `HEAD:…` | 0 | both `6b57424fc5a213a01015beaceb97de47a67967f0` |
| `ls-tree -l` at pin and at `HEAD` | 0 | mode `100755`, size `43497` |
| `git show <rev>:scripts/sources-check.mjs \| sha256sum` at pin, at `HEAD`, and `sha256sum` of the worktree file | 0 | all `6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f` |

`wc -lc` on the pin blob and the worktree file: `897` lines, `43497` bytes.
The C1 content pin matches the committed and working bytes.

Six commits sit after the pin (`rev-list --count` = 6). None touch the script,
and `log 0acb7752..HEAD --grep=sources-check` is empty (exit 0). `diff --name-only 0acb7752 HEAD` is only:

- `1770305` Integrate remote documentation — `LOG.md`, `README.md`, `considerthese/2026-10-19.md`
- `a5683a9` round-34 verifier spot-check — `corpus/lessons/round-34-verifier-spotcheck.md` (new, 17 lines)
- `d933e15` integrator: record verified source-gate direct-file boundary — `SCORECARD.md` (1 line)
- `72d9ccd` considerthese daily reflection — `considerthese/2026-10-19.md`
- `a1a4a38` / `a506dd2` README wiki link — `README.md`, `LOG.md`

`d933e15` does not change the script. It rewrites the `sources-registry`
capability cell from `--selftest` 42/42 to 46/46 and adds the direct-file /
nested-knowledge limit (`SCORECARD.md` capability row, now at line 1616). The
46-case bytes were already the pin; the cell caught up one commit later.

## 2. What kumitate claims, and what it does not plan

Kumitate owns the gate as a product instrument, not as a mutation ledger.

- Province core: the lane's own `scripts/*.mjs` and `corpus/SOURCES.md`,
  checked by `scripts/sources-check.mjs` (`PROVINCE.md:15`). Domain is
  orchestration and tooling (`PROVINCE.md:3`). Refuses anything outside that
  domain (`PROVINCE.md:6`).
- Gate registry owner is "this lane (kumitate L1)" (`SKILL.md:589-595`). The
  sources-check row is an independent gate whose self-test is `--selftest`,
  pinned values live in `corpus/SOURCES.md` plus the frozen `16a5441` legacy
  set, and it is not a `kumitate-proxy-v1` pin (`SKILL.md:605`). Checklist
  items are the live gate and the hermetic suite (`SKILL.md:629-630`).
- The script header describes a hermetic `--selftest` under the OS temporary
  directory and says it does not modify the live tree
  (`scripts/sources-check.mjs:3-8`, usage at `:127`). Contract id in source:
  `kumitate-sources-v1` (`:55`). `git grep -i -e mutation -e mutant -- scripts/sources-check.mjs`
  exits 1 (no matches).

The only mutation claim for this gate is a finished round-34 seat against the
**34-case** suite, recorded in `LOG.md:1420-1433`:

- new gate, "34-case hermetic suite incl. awk-census parity and two cases
  added after the mutation seat's survivors" (`LOG.md:1420-1422`)
- `--selftest` → `SOURCES_SELFTEST: 34/34 pass` (`LOG.md:1430`)
- "Mutation seat: 16 of 18 mutants killed before the fix, the 2 survivors
  killed after it (re-run by the L1 on a /tmp copy: 33/34 FAIL each)."
  (`LOG.md:1432-1433`)

That sentence is the whole mutation record. A repo search for `16 of 18`,
`33/34`, and `mutation seat` hits only `LOG.md:1421-1433` (plus an unrelated
kimi-census mutation seat at `:1442`). `.ufo/rounds/round-34/sources-gate.md`
does not contain the word mutation. Its post-review and parser sections
(`:112-133`) describe behavior fixtures and the direct-only knowledge scan.

Later suite growth is hermetic fixtures, not a new mutation sweep:

| blob | commit | `node <copy> --selftest` | exit | last lines |
|---|---|---|---|---|
| `1a8eed5aaa32043cf109dd28ceb5cd37ccd5555e` | initial landing | 34/34 | 0 | `SOURCES_SELFTEST: 34/34 pass` / `VERDICT: PASS` |
| `06757b0da6c790f823bf765aff366274dc5e1a5a` | post-review | 42/42 | 0 | `SOURCES_SELFTEST: 42/42 pass` / `VERDICT: PASS` |
| `0acb7752d19058b953ebbeba253b1e35f6548de5` | admitted pin | 46/46 | 0 | awk parity `node=4/1/1 awk=4/1/1`; `SOURCES_SELFTEST: 46/46 pass` / `VERDICT: PASS` |

Host `node --version` = `v24.21.0`. Each run was a `/tmp` copy of
`git show <rev>:scripts/sources-check.mjs`, cwd inside the scratch dir. The
46/46 result matches `SCORECARD.md:1616`. The post-review log line is
`SOURCES_SELFTEST: 42/42 pass` (`LOG.md:1536-1538`). The parser-correction
entry (`LOG.md:1550-1562`) adds indented-row and `reflip:` cases and does not
claim a mutation re-run. So the admitted bytes have a hermetic 46-check
selftest and **no** recorded mutation battery.

`LOG.md:1541` ("its mutation rejects `pin.sources-check` as `STANZA_KEY_UNKNOWN`")
belongs to `scripts/proxy-check.mjs --selftest` in the previous sentence
(`LOG.md:1539-1541`). It is not a sources-check mutation case.

No plan to mutation-test this file:

- `SCORECARD.md:437-454` pre-registers round 35 as three claims: K1
  `mcp.json` in `scripts/kimi-census.mjs`, distinct S/R derivation in
  `scripts/proxy-check.mjs`, and R5+R7 sectionization. sources-check is absent.
- `git grep -n -e sources-check -e mutation SCORECARD.md` filtered to lines
  435–1019 (`## Planned` through the line before `## Limits`) printed nothing.
- Clean tree, no extra worktree, no commit message since the pin mentions the
  gate.

Tameshi `PROVINCE.md:61-62` says the gate "landed in kumitate `1a8eed5`". That
is the first introduction (34/34 above), not the admitted bytes. The
integrator spot-check admits the registry capability after recheck at
`0acb775` (`corpus/lessons/round-34-verifier-spotcheck.md:12`, token written
`at0acb775`).

## 3. Domain — Refuses, and whether leg 8 absorbs the gate

Tameshi **Refuses** (`PROVINCE.md:14-17`): product domains; every lane's gate
remains its own; tameshi owns only the reusable craft; a pattern is claimed
general only from evidence in two independent lanes; tameshi never edits a
sibling's gate; recommendations travel in round reports. Same boundary again
at `PROVINCE.md:20` and at Adjacent `PROVINCE.md:44-45` (sibling gate code and
product clauses: report, never absorb).

Tameshi **Owns** the method, with kumitate `scripts/*` named as read-only
primary surfaces (`PROVINCE.md:7-11`). The round-16 append says the recorded
legs are seven, the seventh being `scripts/round-gate.mjs`, probed read-only,
not a service run (`PROVINCE.md:51-57`). The same append already records that
kumitate has seven gates and that `sources-check.mjs` is one of them
(`PROVINCE.md:61-62`). It is named, and it is not yet a recorded leg.

Current ledger (`tools/mutate-and-run.sh:85-91`): three of seven legs are
kumitate scripts (`js-kimi-census`, `js-claims-check`, `js-round-gate`). The
other four are kagi, tsukuroi, and mado. A `js-sources-check` leg makes four
of eight. Replay materializes `git show <rev>:<path>` and does not follow the
sibling worktree (`tools/mutate-and-run.sh:104-109`).

Case 7 is the procedure C1 names. It kept kumitate read-only, cited
`PROVINCE.md:7-11` for "no opt-in", and refused to read the rate as a property
of kumitate's gates in general
(`corpus/knowledge/mutation-case-kumitate-round-gate.md:7-13` and `:136-137`).
Owner recommendations are "reported and not absorbed" (`:148-152`).

That shape does not absorb kumitate's domain:

- The product (orchestration, `corpus/SOURCES.md`, contract
  `kumitate-sources-v1`, the gate's exit map) stays kumitate's
  (`kumitate-shokunin/PROVINCE.md:3-6,15`; `SKILL.md:589-605`).
- A read-only sweep of a byte-pinned copy measures the suite, which is
  tameshi's craft, on a surface tameshi's Owns list and the round-16 append
  already name.
- One more kumitate script does not satisfy the two-lane rule, and case 7
  already forbids narrating a single-gate rate as the lane's gates in general.
  Four kumitate legs out of eight is concentration of primary surfaces, not a
  transfer of the gate.
- Kumitate is not running or scheduling a mutation case on these bytes, so
  the leg does not steal an in-flight kumitate claim. Their mutation sentence
  is closed on the 34-case suite.

Absorption would start if the case edited the sibling file, treated
`kumitate-sources-v1` or `SOURCES.md` as tameshi's contract, filed survivors
as defects tameshi patches, or published the kill-rate as kumitate's mutation
proof of the admitted 46-case gate. The declared case (case-7 procedure,
read-only, travel notes) does not do those. The file's stillness removes a
race: nothing in kumitate's tree is about to invalidate the pin, and a later
kumitate edit would not move a byte-pinned replay.

## 4. Travel-only notes for kumitate

These notes travel. They are not edits, and they are not a request that
kumitate freeze or re-run anything.

1. `scripts/sources-check.mjs` at `0acb7752` is still the worktree and `HEAD`
   blob (sha256 `6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f`,
   mode `100755`). No freeze is needed. A tameshi replay pins those bytes and
   does not follow later commits (`tools/mutate-and-run.sh:104-109` on the
   tameshi side).
2. The mutation seat in `LOG.md:1432-1433` measured the 34-case suite
   (`1a8eed5`, rechecked here as `34/34`). The admitted gate is the later
   46-case file (`0acb7752`, rechecked here as `46/46`; capability cell
   `SCORECARD.md:1616`, updated in `d933e15`). Those are different suites.
   The 46-case file has no recorded mutation sweep. That sweep, if wanted,
   stays this lane's. A tameshi ledger leg is not that sweep and is not a
   change request against `kumitate-sources-v1`.
3. Round 35, as pre-registered (`SCORECARD.md:437-454`), touches
   `kimi-census.mjs`, `proxy-check.mjs`, and runtime section notes. It does
   not schedule `sources-check.mjs`. Nothing to coordinate on this file.
4. `LOG.md:1496-1498` already says the awk-parity case prints SKIP when awk
   is absent. On this host the pinned selftest did not skip (parity
   `node=4/1/1 awk=4/1/1`). An outside rate graded only on process exit can
   look green on a host where that check skips. The limit stays yours.
5. `LOG.md:1541` is proxy-check refusing `pin.sources-check`. It is not
   evidence about this gate's mutants.
6. If a later tameshi report lists survivors, they are suite-gap notes under
   tameshi `PROVINCE.md:14-17`. The gate, the contract, and `corpus/SOURCES.md`
   remain this lane's (`PROVINCE.md:15`).

verdict: holds — sources-check.mjs is unchanged since 0acb7752 (content sha256 matches the C1 pin, porcelain empty); kumitate claims a hermetic 46-check selftest and a closed 34-case mutation seat, and does not plan a mutation case on the admitted bytes; a case-7 read-only leg stays inside tameshi's Refuses clause and does not absorb the gate.
