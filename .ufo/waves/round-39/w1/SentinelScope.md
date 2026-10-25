# SentinelScope — round-39 Scope: fleet-repo untracked sweep

**Verdict: no untracked file in the fleet repo names tameshi round 39.** 0 of 16 untracked
leaves match, under five independent patterns. Every working-tree carrier of "round 39" in
that repo is **tracked** (one modified log, one modified baseline, 46 committed HEAD files).
Nothing was deleted, moved, staged, or edited outside this report.

- Lane root (report base): `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
- Scanned repo: `/home/vgpnk/Projects/shokunin` (fleet) at HEAD `4ae80f41bc9241473d8deb4bba5cc85efa0575b0`
- Observed at `2026-10-24T21:16-03:00` (America/Argentina/Buenos_Aires), re-counted unchanged at `21:17:04`
- Read-only throughout: `git status`, `git diff`, `git grep`, `git ls-tree`, `git check-ignore`, `stat`, `sha256sum`, file reads. No `jj`, no pacman, no installs (none needed).

## 1. Predicate, attacked directly

Exact command, verbatim output:

```
$ git -C /home/vgpnk/Projects/shokunin status --porcelain
 M .ufo/state/chousa.report-baseline
 M .ufo/state/kagi.report-baseline
 M .ufo/state/kaidoku.report-baseline
 M .ufo/state/kake.report-baseline
 M .ufo/state/kama.report-baseline
 M .ufo/state/kengaku.report-baseline
 M .ufo/state/kumitate.report-baseline
 M .ufo/state/mado.report-baseline
 M .ufo/state/mori.report-baseline
 M .ufo/state/souji.report-baseline
 M .ufo/state/tameshi.report-baseline
 M .ufo/state/tsukuroi.report-baseline
 M .ufo/watchdog.log
?? .omp/mcp.json
?? .ufo/state/kotoba.report-baseline
?? .ufo/state/kotodama.report-baseline
?? .ufo/state/revenger.report-baseline
?? bm.json
?? live.html
?? live_s228.html
?? nama.html
?? s395.txt
?? scripts/hyaku/append-closure.py.bak-20261023T040735Z
?? scripts/hyaku/fleet-commit.sh.bak-20261023T040735Z
?? tf_bavelas.html
?? unblob.log
?? wb2.html
?? write
?? xc.xml
```

Content greps over **all 16** untracked leaves, case-insensitive, zero hits for every pattern:

| Pattern | Hits |
|---|---|
| `round[-_ ]?39` | 0 |
| `\bR39\b` / `r39` | 0 |
| `tameshi` | 0 |
| `round[ =._-]?[0-9]+` (any round token at all) | 0 |
| `S107|S108|write-path-census|FLAG_GATE|gates=21|recorded_cases|depth_score|C1_R39|C2_R39|50aadd1b` | 0 |

Completeness of the enumeration: plain `--porcelain` collapses untracked directories, so it was
re-run as `--untracked-files=all`; it returned the **same 16 leaves**. There is no untracked
directory hiding a nested round-39 file. `s395.txt` is 0 bytes (sha256 `e3b0c442…`), so its
filename is the only "39" in the set and it is not a content carrier.

Nearest misses, all **tracked**, therefore outside the predicate:

- `.ufo/watchdog.log:1211` — verbatim:
  `2026-10-24T20:58:13-03:00 launch tameshi round=39 pgid=2253415 driver=hyaku-inline attempt=1`
  (status ` M`, +605 lines this window).
- `.ufo/state/tameshi.report-baseline:1` — verbatim: `39 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
  Comment `39` = round, digest = sha256 of the empty byte stream.
- `.ufo/prompts/tameshi-round-39.md` (`HEAD`, clean, not untracked): line 1
  `You are the tameshi L1, round 39.`; line 158 `**tameshi round 39** (attempt 1;`; line 322–323
  the sanctioned commit `fleet-commit.sh --as tameshi -m "round-39: tameshi report" -- .ufo/reports/round-39/tameshi.md`.
- 46 tracked HEAD paths match `round[-_ =]?39` (`git grep -l … HEAD | wc -l`), including
  `.ufo/reports/round-39/{chousa,kake,kotodama,kumitate,mori}.md`.

## 2. Provenance by time (why the untracked set cannot be round-39 output)

| mtime (-03:00) | Count | Objects |
|---|---|---|
| 18:07:20.648–.653 | 14 | every root artifact (`bm.json`, `live*.html`, `nama.html`, `tf_bavelas.html`, `wb2.html`, `xc.xml`, `s395.txt`, `unblob.log`, `write`, `.omp/mcp.json`, both `.bak-20261023T040735Z`) + `.ufo/state/kotodama.report-baseline` |
| 19:58:12.985 | 1 | `.ufo/state/kotoba.report-baseline` |
| 20:34:33.280 | 1 | `.ufo/state/revenger.report-baseline` |
| **20:58:13** | — | **tameshi round=39 launch (watchdog.log:1211)** |

Fourteen distinct files sharing sub-6 ms mtimes are a bulk restore/copy into the repo root, not
per-round agent writes. The newest untracked file (20:34:33) predates the round-39 launch by
23m40s. The two late baselines belong to kotoba (round 67) and revenger (round 67), per
`watchdog.log` tails, not tameshi.

## 3. Boundary: this command is structurally blind to the lane

`.gitignore:1` is `*-shokunin/`. `git check-ignore -v tameshi-shokunin` →
`.gitignore:1:*-shokunin/`. Two ignored carriers exist:

- `!! tameshi-shokunin/` — the live lane (colocated `.git` **and** `.jj` both present);
- `!! tameshi-shokukin/tameshi-shokunin/` — misspelled scaffold, created Oct 21 02:50, contains
  only an empty `.ufo/` tree, no VCS markers, no `round-39` path.

Consequence, and the reason the negative verdict is not evidence of lane cleanliness: any untracked
file a round-39 seat drops **inside** the lane (including the wave dir written by peers,
`tameshi-shokunin/.ufo/waves/round-39/`) can never appear in this fleet-repo `git status`.
The predicate as assigned covers the fleet repo only; it cannot falsify lane-local strays, and
should not be cited as proof that none exist.

## 4. Sentinel observations on the untracked set (severity / exploit path / remediation)

S-1 (LOW, real, tool-generated) — `.ufo/state`-adjacent stray file named `write`, 25 B,
sha256 `95443b228053f4522714b3ba9cdb56cbce2e2c43b43b073b56e2c70978e0bac0`, content
`agent://U100N079H334f935b\n`. This is the signature of a `write` call that lost its path
parameter: the tool name became the filename and the payload an internal agent URI. Exploit path:
`git add -A`/`git add .` at the fleet root (any manual staging, or a future script without the
current pathspec discipline) publishes an internal agent identifier as repo content; no execution
path (payload is a URI, not a path or shell string). Impact: provenance pollution of the fleet
history, and a permanent leak once pushed. Smallest remediation: owner deletes it or adds an
explicit ignore entry; do not rely on the name being harmless.
Note the guard that keeps it out today: `scripts/hyaku/fleet-commit.sh:45-46` rejects absolute/`..`
paths and refuses `.ufo/state/*` and `.ufo/watchdog.log` pathspecs, and `:77` tracks only the
named filesets with `snapshot.auto-track="none()"` (`:57`) — untracked strays cannot be swept in
by the sanctioned committer.

S-2 (LOW) — two **executable** (0755) backup scripts in the commit-automation directory:
`scripts/hyaku/append-closure.py.bak-20261023T040735Z` (sha256 `0df3f2d8…`) and
`scripts/hyaku/fleet-commit.sh.bak-20261023T040735Z` (sha256 `df65e2f4…`). The `.bak` of
fleet-commit.sh is the **pre-jj** version (its header still documents a git-index implementation,
`diff -u` against the tracked file). Exploit path: a human or script that runs
`git add scripts/hyaku` or packages `scripts/hyaku/*` would ship an executable, stale committer
next to the real one — an operator sourcing the `.bak` would bypass the jj snapshot-safety and
bookmark fast-forward guards at `:57`/`:112-125`. Nothing today globs `scripts/hyaku/*`
(`grep -rn 'hyaku/\*' scripts/` → no glob matches), so this is latent. Remediation: move both to
`$HOME/backups/` or add `*.bak-*` to `.gitignore`.

S-3 (LOW now, MEDIUM if committed) — untracked `.omp/mcp.json` (285 B, sha256 `3439a008…`) is a
project-scope MCP config at the repo root declaring
`rea` = `stdio` / `npx -y rea-agents@6.7.0` / `enabled: false`. Exploit path: if it ever becomes
tracked, any agent session started with cwd = fleet root reads it as project config; enabling it
executes a registry fetch + package run under the operator's account. Version is pinned (`@6.7.0`)
and it is disabled, so no live execution now. Its `$schema` points at a mutable
`raw.githubusercontent.com/can1357/oh-my-pi/main/...` URL (informational only; not fetched by
readers that ignore `$schema`). Remediation: keep MCP config at user scope, or commit it
deliberately with a review of the pinned version.

S-4 (LOW) — four scraped, untrusted bodies sit untracked at the repo root and are **not**
round-39 evidence: `bm.json` (Cloudflare "Just a moment…"), `tf_bavelas.html` (same),
`wb2.html` (Wayback "suspected abusive bot traffic" block), `xc.xml` (Perseus "Too many requests"),
plus `live.html` / `live_s228.html` / `nama.html` (National Museum of Ireland / National
Archaeological Museum pages, one "Page not found"). Exploit path: none by themselves — HTML is
data — but if committed they become repo-trusted content whose provenance (bot-block pages,
museum scrapes) is misread as source evidence. Remediation: delete or ignore scratch `.html`/`.xml`.

S-5 (INFORMATIONAL) — untracked `unblob.log` (1510 B) records a `/tmp/test-fw.bin` extraction with
`Activated FS access restrictions; rules=[Read("/"), ReadWrite("/dev/shm"), ReadWrite("/tmp/unblob-out"), …],
status=FullyEnforced`. It documents sandbox enforcement, not a bypass; no host paths beyond `/tmp`.

## 5. Driver-runtime drift (observed, not mine, already guarded)

13 tracked files are modified in this window (+617/−12): twelve `.ufo/state/*.report-baseline`
counters and `.ufo/watchdog.log`. The tameshi one moved `23 e3b0…` → `39 e3b0…` at `20:58:11`,
2 s before the `round=39` launch line — exactly the launch-time baseline.
`scripts/shokunin-watchdog.sh:110-138` (`record_report_baseline`) hashes
`$UFO/reports/round-$n/$lane.md` and treats a missing report as the empty byte stream, and `:203`
calls it before spawning. So `39 e3b0c442…` is the documented launch convention, **not** fabricated
readiness. Corroboration: `.ufo/reports/round-39/tameshi.md` is absent from both the worktree and
HEAD (HEAD's `round-39/` tree holds only chousa, kake, kotodama, kumitate, mori).
`fleet-commit.sh:46` forbids lanes from committing `.ufo/state/*` and `.ufo/watchdog.log`, so this
drift cannot enter history through the sanctioned path.

## 6. Smallest remediation for the assigned surface

None required for the predicate — it is false and stays false. For hygiene, in ascending cost:
(1) add `*.bak-*`, `write`, and root `*.html` scratch names to the fleet `.gitignore` (one edit);
(2) have the owner relocate the two executable `.bak` scripts and the stray `write` file out of
the repo; (3) decide `.omp/mcp.json` at user scope. All three are owner actions; this seat made
no deletion and no edit outside this report.
