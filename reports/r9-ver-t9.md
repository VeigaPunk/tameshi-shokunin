# VER-T9 — the cadence verifier: independent confirmation of ONE drift event (ER-4 row 3, tsukuroi-census)

Verification run 2026-10-14 19:57–20:06Z by lane VER-T9 (round-9 32-lane wave;
poll `/tmp/w9-ver-t9-poll.log` — 15 s cadence from 19:59:10Z, append detected
20:01:25Z, stable 20:02:55Z; scratch `/tmp/w9-ver-t9-work/`). **Read-only on
every substrate**: the ledger, the tameshi tree, and the tsukuroi/mado trees
were only read; no substrate file was written or edited. The only fleet file
written by this lane is **this report**. No secret file read; no external
site; no substrate-mutating command.

**Artifact under verification.** `tameshi-shokunin/corpus/knowledge/
fleet-kill-rate-ledger.md`. Pre-append baseline sha256
`71bc15e365a3574f48d22c70cdb6d32f6511d5532187886770006e4c6f7b9302`
(315 `wc -l` / 28 503 B; byte-copy `/tmp/w9-ver-t9-work/ledger-before.md`).
The round-9 append was observed in three revisions — `e94633cc…` (351),
`dce68463…` (353), `5ccf95c2…` (353, stable across three samples
20:02:25–20:02:55Z) — then a second block to `2f25c51e…` (363 `wc -l` /
36 169 B) before the binding read. **Append-only proven mechanically:**
`diff ledger-before current` → `315a316,363` (48 added lines, 0 deleted,
0 changed; the pre-round-9 315 lines byte-identical).

**Bound unit.** ER-4 (`:318`), block "Drift events recorded" (`:335`), **row 3
bullet (`:337`)** — bound at ledger sha `2f25c51e…`, span `:316-353` sha256
`2ac5da32ad7c72ff25771b9be2a330704ff34a15ac7936d2c14e686d1c476405`, line 337
sha256 `750f47090d420135ae456e4f549d112f0e2a35f3aaf3efccde279ca85bdcd9fb`
(all read 20:05:07Z):

> - **row 3, tsukuroi `tools/tsukuroi-census.sh`** — `084951be…` @ `165307fe`
>   (round 4) → **`bba6cdf6…`** @ HEAD `72b038d` (round-8 commit). Readable
>   blob chain: `084951be` (`165307fe`) → `aae45531` (`da95290`, round 5,
>   17:33:30Z — the owner hardening §1.3 already records as its replay
>   revision) → `bba6cdf6` (`aa136d6`, round 7, 19:06:31Z). Commit messages
>   are round-generic; the writers are the owner's own lanes.

Plus its pin-read table cell (`:328`): `| 3 | tsukuroi-census | 084951be… @
165307fe | bba6cdf6… (1 472 L / 73 919 B) | yes | clean · yes | stale |`.

## 0. Method (my own commands, not the producer's)

- O **baseline snapshot 19:58:12Z** — all six cases read with my own commands
  (`baseline-1958Z.txt`), taken **before** this lane read any producer scratch.
- O **pin-read harness** `/tmp/w9-ver-t9-work/pinread.sh`: ER-3's published
  command set (`sha256sum <gate-file>`; `git -C <repo> show HEAD:<path> |
  sha256sum`; `git -C <repo> status --porcelain -- <path>`) plus the ancestor
  check `git -C <repo> merge-base --is-ancestor <rev> HEAD`. I executed no
  producer script and took no producer number.
- O **chronology for independence**: baseline 19:58:12Z; between ~20:00:30 and
  20:01Z this lane read the tick lanes' scratch (`/tmp/w9-tameshi-t91/tick.log`,
  `/tmp/w9-tameshi-t93/pin-read.txt`) for wave context only; every cell below
  was then re-derived by re-executing the command at a stated time
  (20:03:47Z / 20:04:22Z / 20:05:07Z).

## 1. Result — claim vs re-derivation (ER-4 row 3)

| cell | ER-4 claim | my re-derivation (O) | match |
|---|---|---|---|
| recorded pin @ recorded rev | `084951be…` @ `165307fe` (round 4) | `git show 165307fe:tools/tsukuroi-census.sh \| sha256sum` → `084951be50bcbfee…c78c5`, 976 ln | ✓ |
| recorded rev ancestor of HEAD | yes | `git merge-base --is-ancestor 165307fe HEAD` → **rc 0** | ✓ |
| live cell | `bba6cdf6…` (1 472 L / 73 919 B) | HEAD blob sha256 → `bba6cdf6f5b7a737…`; `wc -lc` → 1 472 / 73 919 | ✓ |
| live = HEAD blob | yes | live file 19:58:12Z = `bba6cdf6…` = `git show HEAD:<path>` = HEAD blob | ✓ |
| worktree at the tick | clean · yes | my 19:58:12Z read: `git status --porcelain -- <path>` → 0 lines | ✓ |
| blob chain (2 links) | `aae45531` @ `da95290`; `bba6cdf6` @ `aa136d6` | `git show da95290:…` → `aae45531…`; `git show aa136d6:…` → `bba6cdf6…` | ✓ |
| movement set | (chain implies r5 + r7 moves) | `git log --oneline 165307fe..HEAD -- <path>` → exactly `da95290`, `aa136d6`; `72b038d` did not touch the path | ✓ |
| commit stamps | `72b038d` 19:55:09Z · `da95290` 17:33:30Z · `aa136d6` 19:06:31Z | `%cI` → `16:55:09−03` / `14:33:30−03` / `16:06:31−03` | ✓ |

Verdict: **CONFIRMED** — the drift event is real; every ER-4 row-3 cell
reproduces on this host at the bound revisions. (The alternative deliverable —
a no-drift receipt — does not apply: the append records two drift events.)

Precision note (O): `bba6cdf6…` first materializes at `aa136d6` (round 7) and is
carried unchanged by `72b038d`; ER-4's own timing paragraph reads it the same
way ("its gate path was last moved by round 7"). The bullet's "@ HEAD `72b038d`
(round-8 commit)" names the commit that carries the blob, not a round-8 edit.

Later readings (O, recorded; the pin read is a timestamped observation, never a
standing claim): the tsukuroi worktree moved again within minutes — live
`b54f5732…` (1 587 L) at 20:03:47Z, `b6d20a5a…` (1 888 L) at 20:04:22Z, ` M`
both times (the owner's round-9 lane editing). ER-4's clean cell was true at the
tick (my own 19:58:12Z read); the reopening is what ER-4's addendum
(`:356-362`) records at 20:02:38–42Z.

Cross-read (secondary, not the confirmed unit) — row 4, mado: my commands
reproduce its committed-blob cells too (`d7edaab4…` @ `eead56b2`, ancestor
rc 0, HEAD blob `7da4ec50…`, 2 887 L / 131 612 B; chain `c4c1afb7` @ `c8f6667`,
`90d50cdd` @ `0c20a76`, `7da4ec50` @ `12c8f08`; path-touching set
{`c8f6667`,`0c20a76`,`12c8f08`}; `12c8f08` stamp 19:55:09Z). Live 20:03:47Z
`31364115…` (3 215 L, ` M`). I claim only what I re-ran; this is corroboration,
not a second confirmation.

## 2. Spot-checks (three, re-runnable)

- **SC1 — recorded pin + chain links.** Three commands, three shas:
  `git -C tsukuroi-shokunin show 165307fe:tools/tsukuroi-census.sh | sha256sum`
  → `084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5`
  (976 ln); `… show da95290:… | sha256sum` → `aae45531fc393579…`;
  `… show aa136d6:… | sha256sum` → `bba6cdf6f5b7a737…` — the recorded pin names
  the recorded revision's blob, and both chain links verify.
- **SC2 — live cell = HEAD blob + movement set.**
  `git -C tsukuroi-shokunin show HEAD:tools/tsukuroi-census.sh | sha256sum` →
  `bba6cdf6f5b7a7372e43230821bb7c12aa64192266c549f39475c948803a4f55`
  (`wc -lc` 1 472 / 73 919 = the appended live cell);
  `git merge-base --is-ancestor 165307fe HEAD` → rc 0;
  `git log --oneline 165307fe..HEAD -- tools/tsukuroi-census.sh` → `da95290`,
  `aa136d6` only (two moves, r5 + r7; the round-8 commit did not move it).
- **SC3 — write fence + append-only.** `diff ledger-before current` →
  `315a316,363` (48 added, 0 deleted/changed); ledger sha at my reads
  `71bc15e3` → `5ccf95c2` → `2f25c51e` (19:59:10Z → 20:02:55Z → 20:04:22Z; none
  by this lane — read-only); ER-4 row-3 line sha256 `750f4709…` at 20:05:07Z;
  tsukuroi/mado porcelain reads ` M` at 20:03:47Z and 20:04:22Z (owner lanes,
  not this one); tool sha `cf41efaa…` (still held); all evidence under
  `/tmp/w9-ver-t9-work/` and `/tmp/w9-ver-t9-poll.log`; the ledger and both
  sibling trees carry only their owners' writes.

## 3. Unknowns

- **U1 — one unit only.** Row 3 is the confirmed unit; row 4 is a cross-read
  (only the cells listed); rows 1/2/5/6 (`current`) and the regression receipt
  (`:341-348`) were not re-run by this lane.
- **U2 — moving transients unrecoverable.** The gates' worktree readings after
  19:58Z (`b54f5732…`/`b6d20a5a…`/`31364115…`; the addendum's `5d16378d…`/
  `5b6ace8e…`) are superseded on disk within minutes and cannot be re-measured;
  only committed blobs (HEAD-level) are stable, and those are what I confirmed.
- **U3 — revision binding.** My quotes bind to ledger sha `2f25c51e…`
  (20:05:07Z). The ledger is append-only and further appends (the re-sweep
  rows) are expected; ER-4's bytes were stable across my two reads (same line
  numbers, line-337 sha `750f4709…`), but I did not hash span `:316-353` at the
  20:02:55Z read, so byte-identity across those two minutes rests on line
  identity plus the unchanged text.
- **U4 — single host, 2026-10-14.** Load-bearing identities are content shas;
  commit timestamps are the only clock binding, checked only where ER-4 states
  them.
- **U5 — mechanism unknown.** What `bba6cdf6…` actually does (verdicts,
  survivor classes) is ER-4's own [U] — the re-sweep's work, not measured here.
- **U6 — harness not re-run.** I did not execute `--selftest`/`--regression`;
  the ER-4 regression receipt stands on the producer's kept logs
  (`/tmp/w9-tameshi-t91/`) and is outside this confirmation.

## 4. Evidence inventory (`/tmp/w9-ver-t9-work/`)

`ledger-before.md` (`71bc15e3…`) · `ledger-after-2004.md` (`2f25c51e…`) ·
`poll.sh` · `pinread.sh` · `baseline-1958Z.txt` ·
`evidence/pinread-tsukuroi-pre.txt` · `evidence/pinread-mado-pre.txt`;
poll `/tmp/w9-ver-t9-poll.log` (15 s cadence; base → stable → end).

## Errata (append-only)

(none yet — new entries go below this line, never edits above)