# T55W1SentConfig — host-write and network audit (round 55, wave 1)

- Seat: `T55W1SentConfig` (sentinel/config, leaf — no subagent dispatch).
- Judged on: operability. Milestone: host-write and network audit.
- Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`. Audit window: 2026-10-28 ~13:52–14:24 -0300.
- Item: verify the round's changes cannot write outside the lane; read the two tool patches; grep the wave deliverables for writes to `~/.omp`, `/home/vgpnk/.config`, or any fleet path outside the lane; confirm the C2 counter's clone/scratch stay under `--work`; confirm `~/.omp/agent/config.yml` is unmodified (mtime + scout alias).
- Verdict: **PASS on every surface checked. No outside-lane write exists or is proposed.** The traced run has **0** mutating syscalls on the lane, **0** on the fleet root, and **0** on any host-owned path (`~/.omp`, `~/.config`, `~/.local`, `/etc`, `/usr`, `/opt`); the only writes outside `--work` are the measured tools' own `/tmp` scratch in the counter's empty arm (`TMPDIR=""` by design) and `env-diff`'s namespace-local bwrap mounts (§2). The three patched tools write nothing on the refusal path; `~/.omp/agent/config.yml` was not written during the round and still reads `scout: "@m_grok"`; the only outbound network use in the wave is the two documented SOURCES fetches. Adjacent observations are in §5 (reported, not fixes).

Tools installed/upgraded: **none** (no package-manager channel used).

---

## 1. Tool patches — scope and refusal path

The round landed **three** Python patches, not two: `tools/repeat-control.py` (+21/−1), `tools/context-capture.py` (+10/−1), `tools/registry-check.py` (+13/−1) (receipt `01-tools-diff-scope.txt`, `08-tool-patch-scope.txt`). Each diff is exactly three or four hunks, and they are only:

1. a `class ScratchRootUnusable(RuntimeError)` declaration;
2. the single `raise RuntimeError(` → `raise ScratchRootUnusable(` swap inside `strict_scratch_root()`;
3. one handler (two in `registry-check.py`) that writes the frozen grammar line to **stderr** and returns 2 before the generic setup handler can leak the type name.

No other line of those files changes; the worktree tools are byte-identical to HEAD (`git diff HEAD -- tools` empty). The two **drafted** patches (`T55W1ExecRepPatch-receipts/patch.diff`, `T55W1ExecCcPatch-receipts/context-capture.patch`) each name only their own file in `diff --git` / `---` / `+++` and carry the same hunks.

`tools/registry.json` is data-only: 56 rows before and after, names identical, exactly 7 rows differ and only in the `scratch_root` key (the 2301-line diff is re-serialization churn).

Scratch sink: every allocating mode in all seven tools is `tempfile.mkdtemp(..., dir=strict_scratch_root())`; `git grep -c -E 'dir\s*=\s*["'\'']/tmp' HEAD -- tools/` is empty (0 literal `/tmp` scratch sites).

Refusal path (`TMPDIR=<nonexistent>`), measured under `strace -f -y` (receipt `07-registry-check-refusal.txt`):

| tool | rc | stderr | stdout | mutating syscalls |
|---|---|---|---|---|
| `repeat-control.py --selftest` | 2 | exactly 1 line, frozen `GRAMMAR` match | `REPEAT_CONTROL: setup_error` (the tool's own verdict marker) | **0** |
| `context-capture.py --selftest` | 2 | exactly 1 line, frozen `GRAMMAR` match | 0 bytes | **0** |
| `registry-check.py --rev HEAD` | 2 | exactly 1 line, frozen `GRAMMAR` match | 0 bytes | only `/dev/null` `O_RDWR` (Python devnull); no mkdir/symlink/unlink |

The grammar was checked with the *frozen counter's* `GRAMMAR` object (imported read-only), not re-typed. `registry-check.py`'s second handler matters: its pre-existing `except RuntimeError` on the `--rev` path wrote a JSON setup-error report to **stdout**.

Conclusion: the patches only touch their own file's scratch/exit path, and the exit path allocates nothing.

---

## 2. C2 counter — the clone and scratch stay under `--work`

**Static sinks** (counter bytes at the final snapshot `sha256 0458f632…`; identical sink set in the audited bytes, receipt `03-c2-static-sinks.txt`):

- `clone = work / "clone"`, written only by `git clone --shared` + `git -C clone checkout -B r55-rev`;
- `clone/CONTRACT` — the frozen fixture materialized **inside the clone**;
- `work/"tmp-usable"` mkdir; `work/strace-*.log`; `work/c2-receipts.json`;
- `work/envdiff-out.json`, passed as the `env-diff --contract` mode's `--out`.

Every subprocess runs with `cwd=clone`. The only outside root any mode names is `pin-disposition --read --root /home/vgpnk/Projects/shokunin`, a documented **read-only** mode; the trace confirms zero writes there.

**Dynamic audit** (receipt `02-c2-write-audit.txt`, reproducible parser `parse-c2-write-audit.py`): I ran the counter `--lane <lane> --rev 631cd645… --work <W> --explain` under `strace -f -y` over `openat,openat2,creat,mkdir,mkdirat,rename,renameat,renameat2,unlink,unlinkat,symlink,symlinkat,link,linkat,chdir` — 5,109,619 syscall lines (829 MB), 659 s. Classification of every mutating event:

| class | count | meaning |
|---|---|---|
| `work` | ~32,000 | under `--work` (clone, fixture, logs, receipts, `--out`) |
| `tmp` | ~12,000 | tool scratch in the **empty arm** (`TMPDIR=""` → platform default `/tmp`), created and `rmtree`'d by each tool — see nuance |
| `dev` | ~8,000 | `/dev/null` etc. |
| `bwrap-ns` | ~5,000 | `env-diff`'s private mount namespace (`/newroot`, `/proc/<pid>/uid_map`, `/dev/stdin` symlinks) |
| **`lane`** | **0** | — |
| **`HOST-OUTSIDE`** | **0** | — |

Control probe under the identical filter: a write to `<S>/probe-outside2.txt` (outside `W`) is classified `HOST-OUTSIDE`; a write to `<W>/probe-inside2.txt` is `work` — the detector catches what it claims to catch.

**Honest nuances** (not violations):

- The **empty arm deliberately sets `TMPDIR=""`**, so each allocating tool's `mkdtemp` falls back to `/tmp`: those ~12k `tmp` events are the *tools'* scratch, not the counter's. The usable arm's strace census asserts 0 `/tmp` mkdirs and the run printed `tmp_mkdirs=0`. The counter's own entries after the run are only `clone/`, `envdiff-out.json`, `strace-*.log`, `tmp-usable/`, `c2-receipts.json`.
- The `bwrap-ns` events are `env-diff`'s namespace-local mount setup; `/newroot`, `/stdin`, `/stdout`, `/fd` do **not** exist on the host after the run (`ls -d` → ENOENT).
- Under the outer tracer the run scored `empty=12/13 usable=12/13` because `registry-check --selftest` has a timing case that fails under a tracer (rc=1); the unwrapped base rerun (sibling receipt `T55W1ExecNoHarm-receipts/c2-base-rerun.explain.txt`) is 13/13/13. Tracer artifact, not a counter defect.
- The amended counter (freeze amendments 1–8) adds `registry-check --rev` as a **ninth grammar-only allocating mode** and narrows the empty/usable arms to `cheap` modes; it adds no write sink. I audited that new mode's refusal separately (row above): rc=2, stdout empty, no allocation.

---

## 3. Wave deliverables — no proposed write outside the lane

Receipt `05-deliverable-outside-write-sweep.txt`, `05b-git-command-sweep.txt`, `05c-script-sweep.txt`.

- **Shell write commands with an outside target:** none (empty scan).
- **Mutating git:** only fixture drivers, all cloning into `$HYAKU_SCRATCH/tameshi-r55/<seat>/…` and asserting `rev-parse --show-toplevel` equals the clone (`T55W2MutC1/reproduce.py`, `T55W2Read03/driver.sh`, `T55W1RevColdread/commands.sh`, `T55W1ScribeQuality/rescore-positive.sh`). `T55W1ExecReKeyDryBind-receipts/l1-rekey.commands.sh` proposes `git -C "$LANE" add -A .ufo/evidence/round-21/coldread` — a **lane** mutation by the L1 integrator, not an outside-lane write.
- **`~/.omp`:** 63 lines across the wave's markdown (41 × `agent/config.yml`, 12 × `agent/history.db`, plus `mcp.json`, `sessions/`, `agents/`). Every one is (a) the R54.8 incident narration (`T55W1Er08`, `T55W1Rev04`, `T55W1Rev10`, `T55W1Scribe*`), (b) a read-only probe (`sqlite3 -readonly ~/.omp/agent/history.db`; `grep/stat/sha256sum ~/.omp/agent/config.yml`), or (c) the rule forbidding the write ("`~/.omp/agent/` is host state; a seat never writes it"). No deliverable proposes an edit. `~/.config` / `~/.local` appear only as existing-tool paths (`~/.local/bin/jq`) or not at all.
- **Network:** the only outbound use is `T55W1Er10`/`T55W1ScribeSources` fetching `gnu.org` and `man.freebsd.org` for SOURCES rows (documented source fetches; `curl` + `sha256sum` receipts). No round tool or fixture performs network I/O; no deliverable proposes a network write.
- **C1 counter (adjacent, same milestone):** one write sink (`work/c1-derivations.json`); all git calls are `show`, `cat-file`, `ls-tree`, `log`. `--staged-root` (default `/home/vgpnk/Projects/shokuknow`) is still accepted but, after amendment 7, the staged count is read from a committed receipt and the parameter is unused — no outside read or write.

---

## 4. `~/.omp/agent/config.yml`

Receipt `04-config-yml-state.txt`.

- Now: mtime `2026-10-28 13:10:10.791 -0300`, sha256 `51beb75880e5054bfcd6095b61bd600acfc7a85ece74663f663040bc43707418`, size 16624; line 418 `scout: "@m_grok"`.
- Home repo: `MM .omp/agent/config.yml`; worktree-vs-index diff is only `-scout: "@m_zfl"` / `+scout: "@m_grok"` — the index still carries the pre-existing staged `@m_zfl` described in R54.8, not a round-55 action.
- In-round baseline: `T55W1ScribeSeat-receipts/r5-config-state.stdout` (recorded 13:54:09, before this seat ran) shows the **same** mtime and sha → unchanged from 13:54 to this audit.
- Timeline: round-54's last evidence 12:25:37; round-55's first artifact (`no-harm.sh`) 13:33:43, `spec-w1.json` 13:39:49. The file's last write (13:10:10) falls **between** the rounds (23 min before round 55 started, 45 min after round 54 closed).
- No new `config.yml.pre-*` backup (newest 2026-10-27T16:08:23). `config.yml` and `mcp.json` are absent from the `~/.omp/agent` files newer than round start; the newer files there are harness DB state (`agent.db`, `models.db*`, `history.db-shm`), not seat deliverables.

Verdict: **unmodified during round 55; scout alias `@m_grok`.**

---

## 5. Adjacent observations (reported, not fixed, not my item)

1. **The lane moved during this audit.** HEAD went `631cd64` → `e2979f2` (freeze amendments 1–7) → `9cf0146` (C0 integration) → `133b2ce` (amendment 8), with wave-2 work in flight. The assignment's quoted base C2 numbers (`grammar=6/8 … total=18`) are the 631cd bytes; the committed `before/c2.stdout` is now the 9-mode re-measurement (`grammar=6/9 … total=21`). My dynamic audit pins the exact bytes it ran (`9d0768…`); the sink set is identical in the current bytes (`0458f632…`), and `freeze.json` verifies 7/7 files with 8 amendments at the final snapshot. Anyone citing my trace must cite the audited hash, not "the counter".
2. **`repeat-control` still prints `REPEAT_CONTROL: setup_error` on stdout** on the refusal path. It is the tool's verdict marker, not the exception or a traceback, and the C2 predicate (grammar on stderr, rc 2, no `RuntimeError`/`Traceback`) passes. If "stdout carries no setup error" is read as "stdout must be empty", repeat-control and context-capture differ; the counter does not require emptiness.
3. **`context-capture`'s new handler uses a bare `sys.stderr.write`** (no OSError guard, unlike repeat-control's `emit_err`). A closed/full stderr could raise inside the handler; still no outside write.
4. **`tools/registry.json`'s diff is re-serialization** (2301 lines for seven changed cells) — a review-burden churn, not a host-write risk.

---

## Receipts

All under `.ufo/waves/round-55/w1/T55W1SentConfig-receipts/`:
`01-tools-diff-scope.txt`, `02-c2-write-audit.txt`, `03-c2-static-sinks.txt`, `04-config-yml-state.txt`, `05-deliverable-outside-write-sweep.txt`, `05b-git-command-sweep.txt`, `05c-script-sweep.txt`, `06-freeze-and-head.txt`, `07-registry-check-refusal.txt`, `08-tool-patch-scope.txt`, `parse-c2-write-audit.py`.

The 829 MB raw strace log lived only in scratch (`/fast/scratch/hyaku/tameshi-r55/T55W1SentConfig/`) and is removed on seat exit; the classifier and its summary are receipted, so the audit is reproducible from `parse-c2-write-audit.py` + the reported command.
