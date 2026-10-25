# L1Tameshi41.ScoutMisroot — fleet-root untracked-file attribution, round 41 w1

Seat: scout, read-only. Assignment: run `git -C /home/vgpnk/Projects/shokunin status --porcelain`,
decide for every untracked fleet-root file whether it names tameshi and round 41, report with the
grep hit or first line as evidence, delete and move nothing.

Command actually run (four times; the set is live, see "Churn"):

```
git -C /home/vgpnk/Projects/shokunin status --porcelain
```

Marker test applied to every entry:

```
grep -ic tameshi <file>
grep -cE '(round[- _]?41|r41)' <file>        # plus a plain '\b41\b' check for false friends
```

Read-only: this seat wrote no other file, deleted nothing, moved nothing, ran no counter.
Installs: none (no pacman/uv/npm transaction was needed or run; the pacman pause was respected).

## Verdict

**No untracked fleet-root file currently names tameshi and round 41.**
The only current entry that names both is a fleet-run goal doc that *mentions* `tameshi r41`
as an orphaned claim — it is not a tameshi artifact.

One genuine tameshi-r41 artifact **did** appear at the fleet root during the scan and was
already relocated into the lane by its author before this report was written (T2 below).

## Current untracked set (18 entries, snapshot 03:45:08 -0300)

| path | names tameshi | names round 41 | evidence (first line / grep hit) | attributed to |
|---|---|---|---|---|
| `.scratch/goal-20261025-hyaku-12h.md` | **yes** (1 hit) | **yes** (1 hit) | `:56` — `- No report: kake r51, kotodama r69, mado r35, revenger r68, tameshi r41 →` | fleet hyaku run-6 goal doc; names tameshi r41, not an artifact of it |
| `.ufo/reports/round-35/mado.md` | no (0) | no (0) | L1 `# mado round 35 — report`; L3 `Lane: \`mado-shokunin\`. Round: 35 …`; only `41` is L72 `6 files / 41 proposals` | mado r35, **canonical** path (`.ufo/reports/round-<n>/<lane>.md`) |
| `.ufo/state/kotoba.report-baseline` | no | no | L1 `68 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | kotoba round 68 |
| `.ufo/state/kotodama.report-baseline` | no | no | L1 `69 e3b0c442…7852b855` | kotodama round 69 |
| `.ufo/state/revenger.report-baseline` | no | no | L1 `68 e3b0c442…7852b855` | revenger round 68 |
| `.omp/mcp.json` | no | no | L1 `{`; L3 `"$schema": …oh-my-pi…/mcp-schema.json` | tool config (rea server, `"enabled": false`) |
| `bm.json` | no | no | L1 `<title>Just a moment...</title>` (Cloudflare challenge) | web-scrape litter; `.json` extension is wrong |
| `live.html` | no | no | L1 `<!doctype html>`; `<title>National Museum of Ireland Collections Online</title>` | web-scrape litter |
| `live_s228.html` | no | no | L1 `<!DOCTYPE html>`; `"anubis_version" … "v1.26.2"` | Anubis challenge page |
| `nama.html` | no | no | L1 empty; L3 `<!DOCTYPE html>`; `<title>Page not found - National Archaeological Museum</title>` | web-scrape litter (404 page) |
| `s395.txt` | no | no | empty file, 0 bytes | empty write artifact |
| `scripts/hyaku/append-closure.py.bak-20261023T040735Z` | no | no | L1 `#!/usr/bin/env python3`; L2 `"""hyaku append-closure — append one closure entry to MANIFEST.json rounds[]` | hyaku tool backup, 2026-10-23 |
| `scripts/hyaku/fleet-commit.sh.bak-20261023T040735Z` | no | no | L1 `#!/usr/bin/env bash`; L2 `# hyaku fleet-commit — the only way hyaku lane/closure sessions commit to the` | hyaku tool backup, 2026-10-23 |
| `tf_bavelas.html` | no | no | L1 `<title>Just a moment...</title>` (Cloudflare challenge) | web-scrape litter |
| `unblob.log` | no | no | L1 `2026-10-24 02:00.18 [debug] Logging configured extract_root=. pid=125295` | firmware-extraction log (`file=/tmp/test-fw.bin`) |
| `wb2.html` | no | no | L1 `Your request is being blocked because our system has flagged it as suspected abusive bot traffic …` (Wayback Machine) | web-scrape litter |
| `write` | no | no | L1 `agent://U100N079H334f935b` (25 bytes, no newline) | stray tool write; not a report |
| `xc.xml` | no | no | L1 `<!DOCTYPE html>`; body `Too many requests` (Perseus) | web-scrape litter; `.xml` extension is wrong |

Source of the tameshi/round-41 counts is this seat's grep over each file; the "evidence" column
carries the deciding first line or the exact hit.

### Baseline first-token reading (checked, not assumed)

`scripts/shokunin-watchdog.sh:31` defines the format: `.ufo/state/<lane>.report-baseline` holds
`"round SHA256"`; `:117-120` shows it hashes `.ufo/reports/round-<round>/<lane>.md`. Cross-check
against tracked files: `.ufo/state/tameshi.report-baseline` = `41 e3b0c442…`, and the goal doc
places tameshi at r41; mado = `35 …` vs mado r35; kake = `51 …` vs kake r51. So the three
untracked baselines are kotoba r68, kotodama r69, revenger r68 — other lanes, **not** tameshi.
All three carry `e3b0c442…7852b855`, the sha256 of zero bytes (`printf '' | sha256sum`), i.e. the
pre-launch capture taken while `round-<n>/<lane>.md` did not yet exist; the reports now exist
(22067 / 14052 / 20558 bytes). Expected under the watchdog contract, not a defect observed here.

## Transient entries seen, then gone (live churn — reported, not touched)

The fleet-root set changed four times during the scan, so this table records what the first
snapshot contained and what became of it.

### T1 — `?? .ufo/waves/round-35/` → gone at 03:38:41

- Sole file: `.ufo/waves/round-35/w2/reports/RevLogEvidence.md`, 214 lines.
- L1 `# RevLogEvidence — round-35 LOG.md evidence-pointer audit (w2)`; L6
  `Lane root: \`/home/vgpnk/Projects/shokunin/mado-shokunin\`.`
- tameshi 0 hits, round-41 pattern 0 hits (it is mado r35 throughout).
- By 03:38:41 the fleet-root path was gone; `mado-shokunin/.ufo/waves/round-35/w2/reports/RevLogEvidence.md`
  is **tracked and clean in mado's own repo** (`git -C mado-shokunin status --porcelain <path>` empty,
  `ls-files --error-unmatch` succeeds), same 214 lines, mtime 03:38:41.066 (fleet `.ufo/waves` dir
  mtime 03:38:41.068). Reading: the stray fleet-root copy of a mado-tracked report was put back into
  the lane by another actor ~2 ms-wide; bytes matched since mado git reports it unmodified.

### T2 — `?? .ufo/waves/round-41/w1/ReviewScribeEntry.md` → gone at 03:43:53

This is the one artifact in the scan that **names both tameshi and round 41**:

- Appeared at the fleet root at ~03:42: `14763 B`, `221` lines,
  sha256 `d1e0ac472c22c259d08148f96f4140a72e9c3ce61d79f1e9175423338af1eb33`.
- L1 `# L1Tameshi41.ReviewScribeEntry — round 41 w1`; L3 `Reviewed: \`corpus/knowledge/r41-variable-destination-writes.md\``;
  L6 `No counter was run. The live-site check used the tool directly, never \`.ufo/evidence/round-41/census/measure.py\`.`;
  L221 `Report: .ufo/waves/round-41/w1/ReviewScribeEntry.md`.
- The lane path `tameshi-shokunin/.ufo/waves/round-41/w1/ReviewScribeEntry.md` was **absent** while the
  fleet-root copy existed (checked at 03:42) — so this was a misroot, not a mirror.
- By 03:43:49 the lane had its own copy (`17238 B`, `263` lines, sha256
  `174cdd888d9004408f4184fc8839863cc6c912e3efeb11a4e5e4d65c806d05a1` — revised content, not a byte
  copy), and the fleet-root file plus its `w1` dir were gone by 03:43:53. The reporter corrected
  itself; the current status shows no fleet-root tameshi r41 file.

**Why the misroot was silent (inference, high confidence).** The fleet root already carries a
*tracked* `.ufo/waves/round-41/w1/swarm-registry.legacy-wave-v1.json` (`git ls-files` confirms;
`"schema": "ufo-swarm-wave-registry-v1", "wave": "chousa-r41-w1"`, 0 tameshi hits). The directory
therefore exists at the fleet-root relative path, so a seat that resolves its lane-relative
`Report:` trailer against `/home/vgpnk/Projects/shokunin` instead of
`/home/vgpnk/Projects/shokunin/tameshi-shokunin` writes successfully instead of failing with
ENOENT. This is a trap specific to round 41: chousa's wave-1 directory occupies the same
`round-41/w1` path at the fleet root.

## Confidence and remaining unknowns

- **High** — the 18 current entries: each was opened and grep-tested individually; none names
  tameshi and round 41.
- **High** — T2 attribution (`L1Tameshi41`, round 41 in the title, tameshi-lane paths in the body,
  tameshi lane missing the file at the same instant).
- **High** — T1 attribution (mado lane root in the body; tracked-clean mado copy).
- **Medium** — that T1 was moved and T2 was rewritten-then-deleted by their authors; untracked
  files leave no git reflog, so the actor is not recorded.
- **Unresolved** — whether `.ufo/reports/round-35/mado.md` (untracked, canonical name) is waiting
  on a mado closure commit or is a second copy; out of this seat's scope.
- **Unresolved** — whether other seats misrooted earlier in this wave and had their copies removed
  before the first snapshot (03:33). No evidence either way; nothing removed by me.
- Not investigated, and not needed for the question: web-scrape provenance of the 8 challenge/404
  files, or the unblob run behind `unblob.log`.

## Post-report recheck (03:46 -0300, corrected 03:49, after the round-35 scratch notices)

- **No dangling scratch citation here.** This report cites no `.ufo/waves/round-35/scratch/<Seat>/...` path; the one
  `scratch` string in the table is the fleet-level `.scratch/goal-20261025-hyaku-12h.md`, which still exists
  (`[ -e ]` OK). Nothing in this report needed a rebuild, a path-segment fix, or an inline fallback.
- **The one cited lane artifact is intact:** `mado-shokunin/.ufo/waves/round-35/w2/reports/RevLogEvidence.md` — 214 lines,
  `git -C mado-shokunin status --porcelain <path>` empty (tracked, unmodified); `w2/reports/` holds 40 files.
- **Correction (03:49 -0300): that tree was relocated, not deleted.** `mado-shokunin/.ufo/waves/round-35/scratch/` went
  to `scratch-evidence/` and was checkpointed by mado commit `4efaf63` ("round-35: checkpoint the 235 seat evidence
  files and drop the 3.2 GB mutant trees", 2026-10-25 03:43:55 -0300; `git show --stat` = 235 files, 20804 insertions).
  Current tracked count: `git -C mado-shokunin ls-files .ufo/waves/round-35/scratch-evidence/ | wc -l` → **261 files
  across 59 seat dirs** (59 distinct top-level dirs), per-seat mtimes preserved (`scratch-evidence/ConnOverlap`
  03:43:47; tree 03:45:56). The 7 seat dirs I listed at 03:46 were **new** dirs written after the move — `scratch/` is
  untracked (`git ls-files .../scratch/` → 0) and its membership changed again between 03:46:17 and 03:48
  (RevIndex / RevReadmeFrontier / RevRowsUsedBy / ScoutConsiderthese out; RevEntryR15 / RevQuoteS207 / RevScorecard /
  SimplifyRows in). Live churn of a convenience tree, not a rebuild of evidence. This changes nothing above: this
  report cites no path under `scratch/` **or** `scratch-evidence/`, so nothing needed recovery or repointing.
- **Untracked set shrank 18 → 17:** `.ufo/reports/round-35/mado.md` was committed as
  `fed29568 round-35: mado report` (2026-10-25 03:45:27 -0300). The table above is the 03:45:08 snapshot; the remaining 17
  entries were re-listed and still carry the verdict: 0 of them name tameshi and round 41.

Report: .ufo/waves/round-41/w1/ScoutMisroot.md
