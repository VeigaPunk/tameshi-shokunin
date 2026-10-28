# T54W2RevFix03 — C1 fix-pass verify (cats 13–17 anchors)

Seat: `T54W2RevFix03` (wave 2, Godspeed)
Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
C0: `59c38109bf119d0e9d4f878644a82babc937bc1e`
C1: `99c3bc88d704566197783f66b211ee0a830e0330`
Scope: anchor / wording fixes in `### Round-15 gate/probe registry`, `## Live-tree re-pin and entry-command monitor — round 17`, `### Round-17 gate/probe registry — re-pin and monitor`, `### Round-18 gate/probe registry — routed-defect closure` (listed pins `:1731`, `:1852`, `:1853`, `:1879`, `:1958`, `:1961`).

## Axes

1. Citation accuracy — every re-pin resolves at C1 to the claimed bytes.
2. No overstatement — target text supports the citing sentence.
3. QUALITY 104 — no run-together token, missing space, or duplicate parenthetical left or introduced by the hunk.
4. Pin freshness — a moved line count is accompanied by a re-pin (not a silent drift).

## Method

```bash
export TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W2RevFix03
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  diff 59c38109bf119d0e9d4f878644a82babc937bc1e 99c3bc88d704566197783f66b211ee0a830e0330 \
  -- SKILL.md tools/
git -C … show 99c3bc88d704566197783f66b211ee0a830e0330:SKILL.md | sed -n '<lo>,<hi>p'
git -C … show 99c3bc88d704566197783f66b211ee0a830e0330:<cited-file> | sed -n '<lo>,<hi>p'
# pin-disposition TMPDIR arm (C1 blob copied into scratch):
TMPDIR=<unusable-file> python3 pin-disposition.py --selftest   # exit 2, names value
```

Cited tools (`evidence-disposition.py`, `pin-disposition.py`, `mutate-and-run.sh`, `bash-witness-study.py`, `context-capture.py`) are byte-identical C0→C1. `tools/` only changes `tools/env-diff.py` (+3 ScratchRootUnusable arm) — outside this seat’s listed line set; noted, not scored.

Receipts: `.ufo/waves/round-54/w2/T54W2RevFix03-receipts/` (`anchor-checks.txt`, `skill-c0-c1.diff`, `pin-disposition-tmpdir.txt`, `quality104-r15.txt`, `scrub-span.txt`).

## Hunk-by-hunk

### H1 — `### Round-15 gate/probe registry` / SKILL.md:1731 — disposition selftest exit map + QUALITY 104 spacing

- **Severity:** medium (residual QUALITY 104 on the hunk’s context line).
- **C0 → C1:** `exits0/1/2 … and64 … (… 1 case failure or an uncaught setup traceback; round 17)` → `exits 0/1/2 … and 64 … (… 1 case failure, 2 could-not-evaluate — an unusable scratch root or an unreadable input is named, never a traceback; round 54)`.
- **Anchor check (disposition):** `tools/evidence-disposition.py:3231-3233` catches `ScratchRootUnusable`, prints `could-not-evaluate: …`, returns 2 — matches the new parenthetical. Exit map `0/1/2/64` at the tool head still holds.
- **QUALITY 104 on :1731:** repaired (`exits 0`, `and 64`). No duplicate parenthetical.
- **Residual in hunk context (:1730, same paragraph):** `failed/exit1. Help exits0 only as a non-verdict informational mode; context-capture's selftest` — `Help exits0` is the same missing-space class the hunk fixed on the next line; `stays exit2` on :1728 is the same class. Byte-exact quote: `Help exits0 only as a non-verdict informational mode`. Command: `git show C1:SKILL.md | sed -n '1727,1731p'` (receipt `quality104-r15.txt`).
- **Verdict:** motivating stale-traceback claim is fixed; the Round-15 hunk still leaves QUALITY-104 run-togethers on the visible context line.

### H2 — `## Live-tree re-pin` / SKILL.md:1852 — `evidence-disposition.py:460-525` → `:479-544` (+ selftest / docstring re-pins)

- **Severity:** none (fix holds).
- **C1 cell cites:** `tools/evidence-disposition.py:479-544`; selftest `v2-registry-clone-detached-anchor` `:2910-2915` expects exit 0; fixture docstring `:2275` `"anchors at HEAD"`.
- **`sed -n '479,544p'`:** `def resolve_historical_anchor` — bound `refs/heads/<branch>` path, jj-unbound refusal, detached HEAD only when a branch/remote-tracking ref contains it, ends `return "HEAD", commit` at 544. Matches the round-52 bracket.
- **`sed -n '2910,2915p'`:** `historical_case("v2-registry-clone-detached-anchor", 0, …)`.
- **`sed -n '2275p'`:** `"""A detached harness clone anchors at HEAD, not its later remote tip."""`.
- **Verdict:** C0 pins were wrong at the already-grown C0 tool blob; C1 re-pins land on the claimed bytes. No overstatement.

### H3 — `## Live-tree re-pin` / SKILL.md:1853 — `evidence-disposition.py:368-390` → `:385-395`

- **Severity:** none (constants fix holds; see residual on scrub span).
- **C1 cell cites:** `tools/evidence-disposition.py:385-395` for `GIT_NO_REPLACE_OBJECTS=1`, `GIT_GRAFT_FILE=/dev/null`, and scrubbing inherited `GIT_*`.
- **`sed -n '385,395p'`:** G4 comment + `GIT_ENV_OVERRIDES` dict including both named keys (closes at 395). C0 `:368-390` stopped on the opening brace — that defect is closed.
- **Selftests named:** `v2-historical-replace-ref` / `v2-gitdir-env` both expect exit 0 at `:2928-2957`.
- **Verdict:** re-pin covers the named override constants. Scrub *implementation* (`git_environment` filter) sits at `:406-408` (immediately after); comment in-range asserts “without inherited GIT_* state”. Not scored as an overstatement of the constants the w1 finding named; recorded under residual risk.

### H4 — `### Round-17 gate/probe registry` / SKILL.md:1879 — pin-disposition TMPDIR arm

- **Severity:** none (fix holds).
- **C1 cell:** `as the round-13 row, plus exit 2 could-not-evaluate when TMPDIR is set and unusable (round 54: the self-test names the value, no traceback)`.
- **Code:** `tools/pin-disposition.py` selftest path catches `ScratchRootUnusable` → stderr `could-not-evaluate: … TMPDIR is not a usable directory: %r` → return 2 (`:1399-1401` region at C1).
- **Live probe (C1 blob in scratch):** `TMPDIR=<file> python3 pin-disposition.py --selftest` → exit 2, stderr names the TMPDIR path, no traceback (receipt `pin-disposition-tmpdir.txt`).
- **Verdict:** additive arm is true; “self-test names the value” holds; no duplicate parenthetical.

### H5 — `### Round-18 gate/probe registry` / SKILL.md:1958 — bash-witness pin source

- **Severity:** none (fix holds).
- **C0 claim (false):** pinned round-13 bytes “read from `4acc607` through dispositions.json” by the probe itself.
- **C1 claim:** parses `PIN_BASH`/`REV_BASH` from `tools/mutate-and-run.sh:616-617` (`275d8294…`/`fecee874…`); `4acc607` is the `historical_inputs` rev for that tool in `.ufo/evidence/round-18/dispositions.json`, which evidence-disposition reads.
- **`sed -n '616,617p'` mutate-and-run.sh:** `PIN_BASH=275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f` / `REV_BASH=fecee8743e52eb8fb5fbb40782934cb619a1a96e`.
- **bash-witness-study.py:** `PIN_RE`/`REV_RE` compile `PIN_BASH`/`REV_BASH` from the runner; no `4acc607` / dispositions reference in the probe.
- **dispositions.json:** `historical_inputs["tools/bash-witness-study.py"].rev` starts `4acc607…`.
- **Verdict:** overstatement removed; both halves of the new sentence resolve.

### H6 — `### Round-18 gate/probe registry` / SKILL.md:1961 — `lessonround19` → `` `corpus/lessons/round-19.md` ``

- **Severity:** none (fix holds).
- **QUALITY 104:** run-together ASCII token `lessonround19` replaced with a real path.
- **`git cat-file -e C1:corpus/lessons/round-19.md`:** exists.
- **Verdict:** QUALITY37–39 and S049 were already resolving; the third anchor now resolves too. No duplicate parenthetical.

## Findings

### F1 — medium — Round-15 hunk leaves QUALITY 104 run-togethers on SKILL.md:1730

- **file:line:** `SKILL.md:1730` (hunk context for the `:1731` edit).
- **quote:** `Help exits0 only as a non-verdict informational mode`
- **why:** The cats-13 hunk repaired `exits0`/`and64` on `:1731` but left the same missing-space class on the preceding half of the same sentence (`Help exits0`; also `stays exit2` on `:1728`, `failed/exit1` on `:1730`), which the unified diff displayed as unchanged context.
- **command:** `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 99c3bc88d704566197783f66b211ee0a830e0330:SKILL.md | sed -n '1727,1731p'`

## Residual risk / verification gaps

- **H3 scrub span:** `:385-395` covers `GIT_ENV_OVERRIDES`; the filter that drops inherited `GIT_*` is `git_environment` at `:406-408`. Widening the cite to `:385-408` would be belt-and-braces, not required to close the w1 constants defect.
- **`tools/env-diff.py` ScratchRootUnusable arm** is in the C0→C1 diff but outside cats 13–17; not re-audited here.
- No tool install this seat. Pacman untouched. No mutating git/jj anywhere; TMPDIR probes used scratch copies of the C1 blob.

## Artifacts opened

- `SKILL.md` at C0 and C1 (`git show`)
- `tools/evidence-disposition.py` at C1 (ranges 385–410, 479–544, 2274–2276, 2910–2915, 2928–2957, 3231–3233)
- `tools/pin-disposition.py` at C1 (ScratchRootUnusable + selftest handler; live `--selftest` under unusable TMPDIR)
- `tools/mutate-and-run.sh` at C1 (`:616-617`)
- `tools/bash-witness-study.py` at C1 (`PIN_RE`/`REV_RE`)
- `.ufo/evidence/round-18/dispositions.json` at C1 (`historical_inputs` / bash-witness rev)
- `corpus/lessons/round-19.md` at C1 (existence)
- `tools/env-diff.py` C0→C1 diff (out of scope note)
