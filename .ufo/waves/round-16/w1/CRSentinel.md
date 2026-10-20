# CRSentinel — C2 side-effect review of the SKILL.md cold-read snapshot (round 16, wave 1)

Seat: TameshiR16.CRSentinel (sentinel, leaf). Scope: commands that a literal cold-reader of
`.ufo/evidence/round-16/coldread/SKILL.snapshot.md` would run and that write to the lane repo, a
sibling repo, the fleet root, the network or host state. Each one comes with its line number and a
/tmp-mirror substitute, plus a check of wave-1 seats for actual side effects. I edited nothing.
I installed nothing. My only lane write is this report. Scratch: `/tmp/tameshi-r16-CRSentinel-1T12uN/`.

## Pin

- `sha256sum SKILL.snapshot.md` → `97cf436b669ea445abe36cf6757202eec1c2a4bad2814b07f4159bb9dc623580`
  (exit 0). `wc -l` → 1704; the last line has no trailing newline, so `read` shows 1705.
- Lane HEAD `28aeef498cc070c3183271b709bc79d344ff547a`.

## Headline

- **There are no host-state, network or VCS-publishing instructions.** A regex sweep over the whole
  snapshot covered `git (commit|push|add|checkout|stash|reset|…)`, `pacman`, `systemctl`, `sudo`,
  `curl`, `wget`, `npm i`, `uv tool`, `cargo install`, `tee`, `sed -i`, `>>` and `> path`. It found
  no pacman, systemctl, sudo, network fetch, `git commit` or `git push` instruction. The
  `git checkout`/`git restore` hit at L394 is a *prohibition*. "committed at `606716f`" (L1377)
  is a record.
- **The real write surfaces are six:**
  1. one archived script that overwrites frozen evidence (F1);
  2. "read-only" `git status` checks that can rewrite sibling `.git/index` (F2);
  3. a placeholder line that sets `W=/tmp/` when pasted literally (F3);
  4. Appendix A/B relative paths that put driver output in the fleet root (F4);
  5. a lane harness that changed during wave 1 (F5);
  6. record-keeping instructions that write lane corpus/ledger/SHONEN files (F6).
- **Wave 1 caused no mutation that I could detect.** Evidence is under "Wave-1 seat check" below.

## Side-effect inventory (line → effect → /tmp-mirror substitute)

| # | Snapshot line(s) | Command / instruction | Writes to | Sev | /tmp-mirror substitute |
|---|---|---|---|---|---|
| F1 | L1592-1595, L1602 (registry row "do not run"), L1632-1640 | `python3 .ufo/evidence/round-14/capture-context.py` (archived) | **Lane**: atomically replaces frozen `.ufo/evidence/round-14/context-receipt.json`, even on an invalid-input path | High if run (page forbids it) | **Do not execute.** Mark the verdict `not-executed (page forbids; would overwrite frozen receipt)`. Anchor-check by sha only: archive `7313e9a2…7d89`, receipt `05cb55b8…899c1a` |
| F2 | L151-152, L225-226, L350, L381, L535-536, L590, L604-605, L665, L1035, L1056-1058, L1206 (and runbook §0 `operator-runbook.md:52`, named at L1384/L1438) | `git -C <sibling> status --porcelain -- <path>` | **Sibling `.git/index`**: optional index refresh plus `index.lock` | Medium | `git --no-optional-locks -C <repo> status --porcelain -- <path>` (equivalent: `GIT_OPTIONAL_LOCKS=0 git …`) |
| F3 | L543, L611 (forms also at L136, L158, L342, L599) | `W=/tmp/<lane>-r<round>-<n>-work` pasted literally | Shared `/tmp/` root; `-`, `-r`, `-work` files in cwd when files named `lane`/`round`/`n` exist | Medium | `set -euo pipefail; W=$(mktemp -d /tmp/tameshi-r16-<Seat>-XXXXXX)` |
| F4 | L542-555, L557-565, L610-631 | Appendix A/B block run from the fleet root (`cp -p kumitate-shokunin/…` implies cwd = fleet root). The driver contract names `mutant-<id>.mjs`, `evidence/<id>.selftest.txt` and `evidence/results.json` without a directory | **Fleet root** `/home/vgpnk/Projects/shokunin/` if the driver uses relative paths | Medium | `cd "$W"` straight after the copy. The driver resolves every output against `Path(__file__).resolve().parent`. Materialize pristine with `git -C kumitate-shokunin show 175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/kimi-census.mjs > "$W/pristine.mjs"` |
| F5 | L834-836, L935-940, L1002-1003, L1319-1323 | `bash tools/mutate-and-run.sh --target … --workdir <scratch>` / `--regression [--workdir DIR]` / `--selftest`, run from the lane root | `/tmp` by default (mktemp). A relative `--workdir` is `mkdir -p`'d unguarded, i.e. inside the lane. The tool bytes were changing during wave 1 | Medium (transient) | HEAD-blob mirror (recipe below). Always pass an absolute `--workdir "$(mktemp -d /tmp/tameshi-r16-<Seat>-XXXXXX)"`. Record the tool sha256 before and after each run |
| F6 | L230-238 (step 10: note + corpus row), L895-897 (corpus note), L1071-1074 (T1 STALE cell), L1081-1086 (T3 / re-pin appended row), L1239-1244 (appended ledger row), L1470 (`[~]` in SHONEN), L24 (errata) | "Record the sweep…", "an appended row", "Lane assertions use `[~]`" | **Lane**: `corpus/knowledge/*.md`, `corpus/README.md`, `fleet-kill-rate-ledger.md`, `SHONEN.md` | Low-Med | Write to `/tmp/<seat>/lane-mirror/<same relative path>`, seeded with `cp -p` of the lane file. Show append-only with `diff <(git -C tameshi-shokunin show HEAD:<path>) mirror/<path>` |
| F7 | L621 ("note §7 commands") → `mutation-case-kagi-census.md:242`; Appendix A's note → `mutation-case-kimi-census.md:171` | `rm -rf /tmp/tameshi-r3-1-work && mkdir -p …` / `rm -rf /tmp/tameshi-r2-1-work …` | Host `/tmp`: fixed shared path deleted. This contradicts L396-399 (retain scratch as evidence) and refusal (j) at L1267 | Low | Never `rm -rf` a fixed path. Use your own `mktemp -d` dir and rewrite the note's paths onto `$W` |
| F8 | L1062-1067 (drift falsifier) | "a scratch copy of a live gate with one line appended reads `drift`" | A literal reader could append to the **live sibling gate** to get ` M` | Low | `git clone -q --no-hardlinks <sibling> "$W/mirror" && printf '\n' >> "$W/mirror/<path>" && git -C "$W/mirror" status --porcelain -- <path>` |
| F9 | L1492, L1503 | `python3 tools/repeat-control.py --runs 3 --out /tmp/tameshi-r12-controls-UNIQUE -- COMMAND ARG...` | Runs a caller-chosen COMMAND 3×. `--out` is not confined to /tmp (docs only) | Low | `--out "$W/controls"` (must not exist). COMMAND = a selftest or fixture run with cwd = `$W` |
| F10 | L1504 (registry "Write scope: own evidence directory") | `tools/bash-witness-study.py` modes other than the listed `count`/`selftest` | **Lane** `.ufo/evidence/round-12/BashWitness/` by default; `rerun` rewrites `manifest.json`, which is a registry-pinned value | Latent | Only `count` and `selftest` are instructed. Any other mode: `--evidence "$W/bw"` over a copied evidence dir |

Commands I checked as read-only or /tmp-confined (no substitute needed beyond running from `$W`):

- L1535/L1552 `pin-disposition.py`: git `rev-parse`/`cat-file` only (`tools/pin-disposition.py:214-345`); no `status`.
- L1538/L1553 `witness-metadata.py --check`: "No mode writes inside the lane" (`tools/witness-metadata.py:43-45`).
- L1581/L1601/L1681 `evidence-disposition.py`: writes only in selftest `mkdtemp(dir="/tmp")` (`:1512`).
- L1680 `context-capture.py --check`: "Check mode writes nothing" (`tools/context-capture.py:11-12`).
- Every listed `--selftest` uses mkdtemp under /tmp. This includes the temp-repo `git init`/`commit` in `mutate-and-run.sh --selftest` and `pin-disposition.py --selftest`.
- `git config --global --get core.hooksPath` and `init.templateDir` both returned rc=1, and there is no system hook/template config. So the temp-repo commits run no host hooks.

## Findings (sentinel format)

### F1 — the archived capture-context.py overwrites the frozen receipt (High if executed)

- **Exploit path.** A "run every instruction" reader of the round-14/15 sections sees the path in
  L1592-1594, L1602 and L1623, and runs it without arguments.
- **Evidence.**
  - `capture-context.py:23` says "Output: .ufo/evidence/round-14/context-receipt.json".
  - `:46` sets `LANE_ROOT` = 4× dirname of its own realpath, i.e. the lane.
  - `:58` sets `OUTPUT_REL`.
  - `:583-602` `write_receipt` uses `mkstemp` and then `os.replace`.
  - `:614-628` writes the receipt on the InvalidContext path too, so it writes even when it fails.
  - Current shas: archive `7313e9a2…7d89` and receipt `05cb55b8…899c1a`, both equal to the page's
    pins (L1633, L1656), so no wave-1 seat ran it.
- **Impact.** The frozen receipt is destroyed. `context-capture.py --check` (frozen default, L1680)
  then reads `snapshot_tampered`/exit 2, and the round-15 evidence chain breaks. Recovery needs a
  git restore, which is itself a write the page forbids (L394).
- **Smallest remediation.**
  - Wave-2 brief: forbid executing any file under `.ufo/evidence/`.
  - SKILL fix (L1 decision): drop the runnable path from L1602's "Entry command" cell, or add
    "(writes the frozen receipt if run)".

### F2 — "read-only" `git status` can write the sibling `.git/index` (Medium)

- **Exploit path.** Pin/restore checks run plain `git -C <sibling> status --porcelain` while the
  owner lane is editing or committing. Git's optional index refresh takes `index.lock` and rewrites
  `.git/index` whenever any entry's stat data is stale.
- **Evidence (scratch repo `/tmp/tameshi-r16-CRSentinel-1T12uN/repo`).**
  - After `touch f`, `stat .git/index` read `1792502754`. After `git status --porcelain -- f`
    (rc 0) it read `1792502756`, so the index was rewritten.
  - After a second `touch`, `GIT_OPTIONAL_LOCKS=0 git status` and `git --no-optional-locks status`
    left it at `1792502756`, so there was no write.
  - The sibling owner lanes are live: tsukuroi `.git/index` mtime 2026-10-20 10:18:52 and mado
    10:21:51 (owner/fleet activity; not attributed to tameshi).
- **Impact.**
  - It touches sibling `.git`, which the contract says is read-only.
  - It can make an owner lane's `git add`/`commit` fail with `index.lock: File exists`.
  - Worktree bytes, sha and mtime stay unchanged, so the page's restore proof still holds. The
    write is to git metadata only.
- **Smallest remediation.** Change every instructed status call to
  `git --no-optional-locks -C <repo> status --porcelain -- <path>`. The same applies to
  `operator-runbook.md:52`.

### F3 — the literal placeholder sets `W=/tmp/` and keeps going (Medium)

- **Evidence (scratch `…/lit`).**
  - `bash -c 'W=/tmp/<lane>-r<round>-<n>-work; echo "rc=$? W=[$W]"'` printed
    `bash: line 1: lane: No such file or directory`, then `rc=1 W=[/tmp/]`. The assignment
    survives the redirection failure.
  - With files named `lane`, `round` and `n` in cwd, the result was `rc=0 W=[/tmp/]`, and files
    `-`, `-r` and `-work` were created in cwd.
- **Exploit path.**
  - Without `set -e` the block continues. `mkdir -p "$W/evidence"` creates `/tmp/evidence` and
    `cp -p … "$W/pristine.mjs"` writes `/tmp/pristine.mjs`.
  - `python3 "$W/mutate_driver.py"` then **executes `/tmp/mutate_driver.py`**, a shared
    world-writable location another seat may have written.
  - Parallel wave-2 seats would overwrite each other's pristine copies and evidence, and the
    results would cross-contaminate.
- **Impact.** Corrupted parallel evidence, plus execution of a foreign file. With the edge-case cwd
  files it also writes into the repo.
- **Remediation.** In the wave-2 brief, require `set -euo pipefail; W=$(mktemp -d /tmp/tameshi-r16-<Seat>-XXXXXX)`.
  SKILL fix: put `set -euo pipefail` and a mktemp form at the top of both blocks.

### F4 — Appendix A/B output paths are unanchored, so output can land in the fleet root (Medium)

- **Evidence.**
  - L545 and L613 use fleet-relative inputs (`kumitate-shokunin/…`, `kagi-shokunin/…`), so the
    reader's cwd is the fleet root.
  - L557-565 tell the driver to "write `mutant-<id>.mjs`", "save stdout → `evidence/<id>.selftest.txt`"
    and "aggregate `evidence/results.json`" without naming a directory.
  - L627 says the Appendix B run's cwd is the work dir, but neither block contains a `cd`.
  - The L553-554 probes imply `$W/mutant-*`.
- **Impact.** A literal driver writes about 10 mutants plus `evidence/` into
  `/home/vgpnk/Projects/shokunin/`, which is outside the lane root and prohibited.
- **Related read hazard (not a write).** The kumitate worktree has drifted:
  `sha256sum kumitate-shokunin/scripts/kimi-census.mjs` → `5e8d5913…` against the pin `83016d45…`.
  The `git show 175de6ba:…` blob still equals the pin. Kagi's worktree still equals its pin
  `275d8294…`, and its blob mode is `100755`.
- **Remediation.** Add `cd "$W"` to both blocks, and "all driver paths are relative to `$W`" at L557.

### F5 — the lane harness changed during wave 1 (Medium, transient)

- **Evidence.**
  - 10:27:20: `sha256sum tools/mutate-and-run.sh` → `2e810b5d…a7c6`, 1668 L, ` M`, with
    `TABLE_ROUNDGATE='@@R16_ROUNDGATE_TABLE@@'` (:569) and `@@R16_ROUNDGATE_SPEC@@` (:904).
  - 10:27:45: back to `75ed934d…adc5`, which equals `git show HEAD:tools/mutate-and-run.sh`.
  - A staging copy exists at `.ufo/waves/round-16/w1/RGLeg.mutate-and-run.sh` (10:28:43).
  - I messaged TameshiR16 about this.
- **Exploit path.** A seat executing L935/L1002/L1319 from the lane root in that window ran
  in-flight bytes. A red result or a placeholder SETUP there is a harness artifact, not a page
  defect.
- **Other harness write facts.**
  - `--workdir` is `mkdir -p`'d with no path guard (`mutate-and-run.sh:420-424`, `:1088-1094`).
  - Suites run via `bash -c "$SUITE"` in the caller's cwd with no `cd` (`:393-395`). Mutated
    sibling gates therefore run with the reader's cwd. [INFERENCE] This matters only if a mutant
    breaks its suite's hermeticity; I observed none.
- **Mirror recipe (I built it but did not run the tool, because my seat may not run lane code).**

  ```bash
  S=$(mktemp -d /tmp/tameshi-r16-<Seat>-XXXXXX)/fleet
  mkdir -p "$S/tameshi-shokunin/tools"
  for r in kumitate-shokunin kagi-shokunin tsukuroi-shokunin mado-shokunin; do
    ln -sfn /home/vgpnk/Projects/shokunin/$r "$S/$r"
  done
  git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show HEAD:tools/mutate-and-run.sh \
    > "$S/tameshi-shokunin/tools/mutate-and-run.sh"   # sha must be 75ed934d…
  cd "$(mktemp -d /tmp/tameshi-r16-<Seat>-run-XXXXXX)"
  bash "$S/tameshi-shokunin/tools/mutate-and-run.sh" --regression --workdir "$PWD/regression"
  ```

  What I checked:
  - `SELF=$(readlink -f …)` at `:158`, so FLEET_ROOT resolves to the mirror: I computed
    `/tmp/tameshi-r16-CRSentinel-1T12uN/fleet`.
  - `git -C "$S/kagi-shokunin" rev-parse --verify fecee874…^{commit}` → ok.
  - `git -C "$S/kumitate-shokunin" cat-file -e 175de6ba…:scripts/kimi-census.mjs` → ok.

  The `--regression` run itself is untested by me.

### F6–F10

These are in the inventory table above. They are bounded and need no extra evidence, beyond:

- F7's targets are currently absent (`ls /tmp/tameshi-r2-1-work /tmp/tameshi-r3-1-work` → No such
  file), so nothing is lost today.
- F9's collision is fail-closed (`repeat-control.py:24-25`, `:315-317`: an existing `--out` →
  exit 64).

## Wave-1 seat check (what actually happened)

- **Lane tree.** `git --no-optional-locks -C tameshi-shokunin status --porcelain` showed:
  - ` A .ufo/evidence/round-16/coldread/SKILL.snapshot.md`: staged. Someone ran `git add`;
    presumably L1, unverified.
  - `?? .ufo/evidence/round-16/census-start.txt`
  - `?? .ufo/waves/round-16/`
  - the transient ` M tools/mutate-and-run.sh` (F5).

  No corpus, ledger or SHONEN write was seen (F6 clean).
- **Siblings.** All of kumitate, kagi, tsukuroi and mado are porcelain-clean
  (`--no-optional-locks`), with no `index.lock`.
  - CR11a (`w1/CR11a.md:18,57,75`) and CR11b (`w1/CR11b.md:28,87`) ran **plain**
    `git -C kumitate-shokunin status --porcelain`.
  - kumitate `.git/index` mtime is still `2026-10-19 22:11:01`, so no index write actually
    happened (no stale stat). The F2 hazard was present, but there was no mutation.
- **Frozen evidence.** The round-14 receipt, archive and negative fixture all equal the page's pins
  (F1 not triggered).
- **Shared /tmp.** `/tmp/evidence`, `/tmp/pristine.mjs`, `/tmp/pristine.sh`, `/tmp/mutate_driver.py`,
  `/tmp/empty-root` and `/tmp/<lane>*` are absent, so F3 was not hit.
- **Fleet root.** `find -maxdepth 2 -newer SKILL.snapshot.md` for `mutant-*`, `pristine*`,
  `evidence`, `*CR*` and `*tameshi*` returned nothing.
  - Recent fleet-root changes are `MANIFEST.json`, `.git` commit, `.ufo/state/*.report-baseline` and
    `.ufo/watchdog.log`. These are fleet-driver activity.
  - `.ufo/waves/round-16/build/advice/RevengerPlannerWalk.md` is another lane's. None of these is
    attributable to tameshi seats.
- **Scratch hygiene (low).**
  - Several seats used predictable names rather than `mktemp -d`. Six seats share the suffix
    `-3092` (CR01, CR03, CR08, CR14, RGControl, RGMatrix); others are `-a`, `-1`, bare
    `tameshi-r16-CR07`, `-RGSpecC/D/E`.
  - A few fall outside the `/tmp/tameshi-r16-<YourName>-*` shape: `tameshi-r16-probe.SrkhEe`,
    `tameshi-r16-survivorprep`, `tameshi-r16-cr12b-work`.
  - The risk is theoretical on a single-user host.
- **Anchors no longer checkable (for verdict adjudication, not side effects).** The page's /tmp
  evidence anchors are gone, probably wiped from /tmp [INFERENCE]: `/tmp/w6-aud-t6-work`,
  `/tmp/w7-tameshi-1`, `/tmp/w8-tameshi-t84`, `/tmp/w9-tameshi-t93`, `/tmp/w10-t10-4-ev`,
  `/tmp/w11-t11-4-ev`, `/tmp/tameshi-r2-1-work`, `/tmp/tameshi-r3-1-work`. A seat that can't
  re-check them has an unavailable anchor, not a false claim.

## Wave-2 brief block (paste-ready)

```
Side-effect rules for executing SKILL.snapshot.md (CRSentinel w1):
1. Start every replay with: set -euo pipefail; W=$(mktemp -d /tmp/tameshi-r16-<Seat>-XXXXXX); cd "$W"
   — never paste W=/tmp/<lane>-r<round>-<n>-work literally (it sets W=/tmp/).
2. Sibling bytes: git -C <repo> show <rev>:<path> > "$W/…" ; sibling status checks ONLY as
   git --no-optional-locks -C <repo> status --porcelain -- <path>.
3. Driver/mutant/evidence paths resolve against $W, never cwd; never run from the fleet or lane root.
4. mutate-and-run.sh: run the HEAD-blob mirror (CRSentinel F5 recipe), absolute --workdir under $W,
   record tool sha256 before/after.
5. Never execute anything under .ufo/evidence/ (capture-context.py overwrites the frozen receipt).
6. Never rm -rf a fixed /tmp path from a note's reproduce block; rewrite onto $W.
7. Record/append instructions (note, corpus row, ledger row, SHONEN [~], errata) go to
   $W/lane-mirror/<relpath>; show append-only by diff against git show HEAD:<relpath>.
8. Drift demo: on a git clone --no-hardlinks under $W, never on a live gate.
```

## Recommendations (bounded; L1 decides, I edited nothing)

1. Brief wave-2 seats with the block above (F1–F8).
2. For seats that ran lane-root `mutate-and-run.sh` around 10:26–10:28, ask for their before/after
   sha256 before crediting or debiting the L929-1008/L1302-1363 sections (F5).
3. Candidate SKILL.md repairs for L1, each a one-line edit:
   - add `--no-optional-locks` to the status commands (F2);
   - add `set -euo pipefail` and `cd "$W"` to the Appendix A/B blocks, and "paths relative to `$W`"
     at L557 (F3/F4);
   - mark L1602's archived path "writes frozen receipt if run" (F1).

## Commands executed (all exit 0 unless noted)

- `sha256sum`, `wc -l` on the snapshot.
- `git rev-parse HEAD` in the lane.
- `git --no-optional-locks -C <5 repos> status --porcelain`, plus `stat` on each `.git/index`.
- Scratch git index experiment in `/tmp/tameshi-r16-CRSentinel-1T12uN/repo`.
- Literal-placeholder experiment in `…/lit`.
- `ls` of `/tmp` placeholder targets and historical scratch (exit 2: absent, expected).
- `find` at the fleet root (my first `-newermt '-3 hours'` form errored, exit 1; rerun as
  `-mmin -240`).
- `sha256sum`/`wc`/`stat` of `tools/mutate-and-run.sh` at 10:27:20 and 10:27:45, and
  `git show HEAD:tools/mutate-and-run.sh | sha256sum`.
- Mirror build: `ln -s`, `git show` into /tmp, a `readlink -f` computation, `git rev-parse` and
  `git cat-file` through the symlinks.
- `git config --global/--system` hook/template queries (rc 1: unset).
- `sha256sum` of the three round-14 files.
- Sibling pin checks: `sha256sum` of the kagi/kumitate worktree gates, `git show fecee874:… | sha256sum`,
  `git ls-tree`.

## Opened

- `.ufo/evidence/round-16/coldread/SKILL.snapshot.md` (full)
- `tools/{mutate-and-run.sh,bash-witness-study.py,context-capture.py,evidence-disposition.py,pin-disposition.py,repeat-control.py,witness-metadata.py}` (grep and partial reads)
- `.ufo/evidence/round-14/capture-context.py` (grep)
- `corpus/knowledge/operator-runbook.md`, `mutation-case-kagi-census.md`, `mutation-case-kimi-census.md`,
  `mutation-case-kagi-checklist.md`, `mutation-case-tsukuroi-census.md` (grep for side-effect patterns only)
- `.ufo/waves/round-16/w1/CR*.md` (grep for status/harness/placeholder commands only, to check wave-1 seats)

Tool installs: none.
