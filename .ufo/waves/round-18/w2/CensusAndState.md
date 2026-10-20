# CensusAndState — round 18 wave 2 (FALSIFY)

Read rev: `01d586ddbc5fcd78659557c4e93a6ee8517b87d1` (lane HEAD, detached; working tree matches this rev for `corpus/SOURCES.md`).
Scope: census counts, lane/fleet state, misroot scan. No edits to lane files, no git/jj writes, no tool installs. Scratch work only under `/tmp/tameshi-r18w2-CensusAndState-*`. The only lane write is this file.

## 1. `sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`

Command and exit:

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
tameshi	W04	S047 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	W04	S048 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	ok	/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md
EXIT=0        # 3 lines exactly (verified with wc -l)
```

- Exit 0 with W-codes is the documented contract: `scripts/sources-census.sh:16` — `exit: 0 clean or warnings · 1 E/overdue findings …`; line 33 documents W04 as a warning that "do not affect clean lanes". The script's own selftest asserts the same (`:361-365`, `W04-does-not-fail-validation` expects exit 0).
- **The two W04 lines are by construction, not drift.** Rows S047/S048 are the deliberate same-URL precision chain: `corpus/SOURCES.md:56` (S047) and `:57` (S048) at 01d586, explained at `:200-201` ("same PIT URL, no new source"). They have different scopes, so they do not trip E04; W04's condition (`scripts/sources-census.sh:644-645`) has **no** `supersedes` exemption, unlike E04 (`:646-649`). A lane in this state can therefore never print zero validation lines.
- **W04 predates round 18.** Validate against the *archived corpus at 183f87b* (see §2 method) prints the identical three lines and exits 0. Nothing here is new in this wave.

## 2. Frozen manual row census (183f87b vs 01d586)

Method (independent of the census tool): extract `corpus/SOURCES.md` with `git show <rev>:…`, parse the `## Registry` section with `awk -F'|'` (`$5`=tier, `$9`=status), cross-check row counts with `grep -c '^| S[0-9]'`, then re-run the census script over a per-rev archived corpus (`git archive <rev> corpus | tar -x -C $T/<rev>/tameshi-shokunin`, plus a two-line `shokunin.conf` naming the lane) so that E11/used-by resolution is faithful to that rev. All three methods agree.

| rev | lines | rows | tier A | tier B | tier C | mined | queued | rejected | invalid |
|---|---|---|---|---|---|---|---|---|---|
| 183f87b | 195 | **62** | 54 | 6 | 2 | 35 | 24 | 3 | 0 |
| 01d586d | 208 | **72** | 63 | 7 | 2 | 44 | 23 | 5 | 0 |

File identity: `sha256(183f87b:corpus/SOURCES.md)` = `ac82b2df0ffd44f4e3e74e90cdae2a2eac6bc72ed557dd428c45397f97c828d5`; `sha256(01d586:…)` = `1d4b5910d2ef3e4acbf09a0dfaab61f5ba0e979fb8bc1c99d7241eee5d274e37`; working-tree file hashes to the same `1d4b5910…`, and `git hash-object` (`94ff6dc82b501830f5c6836c6c0c82ed3d559b64`) equals `git rev-parse 01d586:corpus/SOURCES.md`, so the live file is the read-rev file.

Per-row composition of the +10 rows (id-level diff, not histograms):

- Added: `S065`–`S074` only; no id removed. New rows: tier A 9, tier B 1 (`S070`); status mined 8, rejected 2 (`S067`, `S071`).
- Changed existing row: `S008` `A/queued` → `A/mined` (row cited by C1's entry). No tier changes, no other status changes.
- Arithmetic checks: 62+10=72; tiers 54+9=63 / 6+1=7 / 2=2; statuses 35+8+1=44 mined, 24−1=23 queued, 3+2=5 rejected.
- Registry section spans heading `## Registry` at line 8 in both revs, next heading at `:180` (183f87b) / `:192` (01d586); rows occupy contiguous lines 12–73 (62) and 12–83 (72), which is why E01/E12 produce nothing.

The census script's own `census` mode over those archived corpora returns exactly these totals at both revs (`rows 62`/`72`, `FLEET.rows` identical, `tier.invalid 0`, `status.invalid 0`, `missing 0`, exit 0).

## 3. `jj-lane.sh state` and lane porcelain

```
$ /home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh state /home/vgpnk/Projects/shokunin/tameshi-shokunin
state branch=master local=01d586ddbc5fcd78659557c4e93a6ee8517b87d1 remote=01d586ddbc5fcd78659557c4e93a6ee8517b87d1 ahead=0 behind=0 head=detached tracked=0 untracked=8
EXIT=0        # repeated 2 s apart at 20:28:39Z / 20:28:41Z: identical
```

Field semantics verified in `scripts/hyaku/jj-lane.sh`: `local`/`remote` are `refs/heads/$branch` and `refs/remotes/origin/$branch` (`:169-170`), `head` is git `symbolic-ref` state (`:175`), `tracked`/`untracked` are porcelain line counts (`:177-178`). `refs/remotes/origin/master` exists and equals `refs/heads/master`, so `ahead=0 behind=0` are real counts, not the `|| echo 0` fallbacks (`:173-174`). `head=detached` is accurate: HEAD is detached at the same commit as the `master` tip (`git rev-parse HEAD` = 01d586…, `@{upstream}` → "fatal: HEAD does not point to a branch"). `cmd_state` is documented as "pure git, read-only; no jj calls" (`:155`), consistent with the lane-safety rule.

Lane porcelain (list only), first snapshot:

```
$ git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin status --porcelain
?? .ufo/waves/round-18/assignments2.json
?? .ufo/waves/round-18/dispatch2.json
?? .ufo/waves/round-18/record2.json
?? .ufo/waves/round-18/spec2.json
?? .ufo/waves/round-18/w2/
EXIT=0        # 5 lines, all untracked; jj-lane reported untracked=5
```

**The count is live, not a fixture.** During this run sibling seats wrote the lane, and the same command grew to 8 untracked entries, all `??` (no tracked modifications):

```
$ date -u +%FT%TZ; git status --porcelain        # 2026-10-20T20:28:39Z
?? .ufo/evidence/round-18/coldread/traces/
?? .ufo/evidence/round-18/sources-check/survivor-probes/
?? .ufo/waves/round-18/assignments2.json
?? .ufo/waves/round-18/dispatch2.json
?? .ufo/waves/round-18/record2.json
?? .ufo/waves/round-18/spec2.json
?? .ufo/waves/round-18/w2/
?? corpus/lessons/round-18.md
EXIT=0
```

Observed `untracked` progression for `jj-lane.sh state`: 5 → 6 → 8 over the working window (new paths: `…/survivor-probes/`, `corpus/lessons/round-18.md`, `…/coldread/traces/`). Conclusion: `tracked=0` is a stable, checkable fact (the tree has no tracked modifications); `untracked` is a racing target and must not be pinned to an exact value in any acceptance rule. This report lands inside the already-untracked `w2/` directory and adds no new porcelain line.

## 4. Fleet-root status and misroot scan

```
$ git -C /home/vgpnk/Projects/shokunin status --porcelain      # 2026-10-20T20:28:57Z, 10 lines
 M .ufo/watchdog.log
?? .ufo/state/kaidoku.report-baseline
?? .ufo/state/kake.report-baseline
?? .ufo/state/kama.report-baseline
?? .ufo/state/mado.report-baseline
?? .ufo/state/mori.report-baseline
?? .ufo/state/souji.report-baseline
?? .ufo/state/tabi.report-baseline
?? .ufo/state/tameshi.report-baseline
?? .ufo/state/tsukuroi.report-baseline
EXIT=0
```

Content scan over every untracked fleet-root file (`git ls-files --others --exclude-standard`, 9 files at the final snapshot):

- `grep -qi 'tameshi'` → **zero hits**; two-signal scan (`tameshi` AND `round[ -]?18`) → **zero hits**.
- Each `*.report-baseline` is 68 bytes, content `<int> <sha256>` with the sha256 of the empty string (`e3b0c442…b855`); `tameshi.report-baseline` = `18 e3b0c442…b855` (sha256 `12c1c7c85c4040186cfb84c1f5da7d76f3dc03101d0caf72924870300a6a338c`). It names tameshi only in its filename and is one of nine sibling lane baselines in the fleet-level `.ufo/state/` — not a lane artifact.
- One round-18 fleet-root file did appear mid-run and was flagged by a naive content grep: `.ufo/reports/round-18/tsukuroi.md` (19902 bytes, mtime 17:28, listed `??` at ~20:26). It is **not** a tameshi misroot: `grep -i tameshi` on it is empty (the 17 hits are `round18`/`R18` for tsukuroi), and `.ufo/reports/round-N/<lane>.md` is the fleet's canonical report drop (tracked precedent `.ufo/reports/round-1/tsukuroi.md`; rounds 17/19 reports committed at `5434376`/`3a4d1aa`). It was committed as `0b469d1 round-18: tsukuroi report` during this run and no longer appears untracked.

**No untracked fleet-root file names tameshi round 18; no misroot found.** The only caveat is empirical: a content-only `round-18` grep at fleet root false-positives on other lanes' reports (here, tsukuroi's), so a misroot gate must require the lane token too.

## 5. Calibration hazards observed (non-blocking; no defect claim)

1. **Out-of-lane `--file` manufactures E11.** `resolve_targets` derives the lane directory from the registry file's grandparent (`scripts/sources-census.sh:501`) and E11 checks `<dir>/<used-by>` (`:567`). Copying `corpus/SOURCES.md` to `/tmp/.../b.md` and running `validate --file` therefore reports every used-by path as missing: executed → exit 1, 69 lines = 2 W04 + **67 E11**. A frozen-rev reproduction must archive the whole `corpus/` at that rev (as done in §2); otherwise 67 false errors are produced. Documenting this, or adding an explicit `--lane-dir`, would prevent the misreading.
2. **`untracked` is not fixture-stable** (§3): 5 → 6 → 8 within minutes while sibling seats write. `jj-lane.sh state`'s `untracked=` and raw porcelain should be compared as sets/allowlists, never equality, in wave grading.
3. **W04 is a permanent warning in this lane** (§1). Any criterion phrased as "validate prints nothing" fails forever; the current, documented criterion (exit 0 with W-codes) is met.

## Commands exercised (all read-only; no tool installs, no upgrades)

- `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` (exit 0, 3 lines); `census`/`validate` over `git archive` corpora at 183f87b and 01d586 (each exit 0; 62/72 rows).
- `scripts/hyaku/jj-lane.sh state …/tameshi-shokunin` (exit 0; run twice 2 s apart).
- `git -C <lane> status --porcelain` (exit 0; 5 → 8 untracked entries; no tracked modifications); `git -C <fleet> status --porcelain` / `-uall` (exit 0; 1 M + 9 untracked).
- `git show`/`git archive`/`git hash-object`/`git rev-parse`/`git ls-files --others` (read-only), `awk`/`grep`/`sha256sum` census cross-checks.

**Verdict: holds** — the 62→72 row census (A 54→63, B 6→7, C 2→2; mined 35→44, queued 24→23, rejected 3→5; +S065–S074, S008 queued→mined) reproduces under three independent parsers, `validate` exits 0 with only the by-construction S047/S048 W04 pair at both revs, lane state is `master=origin/master=01d586d` with `head=detached`, clean tracked tree and sibling-driven untracked drift, and no untracked fleet-root file names tameshi round 18 — with the two non-blocking calibration hazards (out-of-lane `--file` yields 67 phantom E11; `untracked` count races live writers).
