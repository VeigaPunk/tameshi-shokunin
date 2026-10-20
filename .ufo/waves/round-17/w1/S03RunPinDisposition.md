# S03 — run pin-disposition registered commands at the branch tip

Lane rev: `98bea7da5801f4bc58e4187690ee1687c8a5061f` (detached HEAD at `refs/heads/master` tip).
Tool under test: `tools/pin-disposition.py`, sha256 `297253971dab3a558b470a04162b9d768287844dc0e81bf41a1f9f263ff14f11`.
That digest equals (a) the working-tree file, (b) `git show HEAD:tools/pin-disposition.py`,
(c) `tool_sha256` in the live output, and (d) the round-13 pin in
`.ufo/evidence/round-13/expected.json:9`. No tool install/upgrade was performed.

## Axes (godspeed)

1. **Operability** — do the registered entry and selftest commands return their registered
   outcomes at the branch tip, including on the jj-style detached-HEAD layout?
2. **Calibration** — is the observation dated and drift-explicit, so a count-stable rerun
   cannot be mistaken for an unchanged observation?
3. **Evidence fidelity** — are the digests/HEAD facts independently corroborated and are
   unexercised branches left unexercised?

## Commands and exits

The only registered source at this rev is the SKILL.md row
(`SKILL.md:1552`, recipe `SKILL.md:1535`). `tools/registry.json` does **not** exist at
`98bea7da` (`ls tools/registry.json` → No such file), so the machine registry (R16-MON1)
cannot yet grade this row.

| # | Command (cwd = lane root) | Registered outcome | Observed | Exit |
|---|---|---|---|---|
| 1 | `python3 tools/pin-disposition.py --selftest` | PASS; failure code 1 only if a case fails | `SELFTEST: PASS (18/18)`, 18 case lines `PASS` (`unchanged` … `invalid-root`) | **0** |
| 2 | `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin` | 0 observations, including changed/unavailable | `status: ok`, `counts {legs:6, unchanged:3, changed:3, unavailable:0}`, `observed_at 2026-10-20T15:21:25Z` | **0** |
| 3 | (extra) same with `--manifest /tmp/does-not-exist-r17.json` | 2 invalid input/could-not-evaluate | `status: invalid_input`, `error.kind: invalid_manifest`, `legs: []` | **2** |

Exit-map branches not exercised: the selftest failure code 1 (no case failed, so this is
*not exercised*, not "passed"), and the "root not a directory" path (selftest case
`invalid-root` covers it in fixtures only). Probe exit 0 covers drift and unavailable legs
by design (docstring `tools/pin-disposition.py:68-71`), so exit 0 is not a clean-content
claim.

No temp residue from the selftest: `ls -d /tmp/tameshi-r13-pin-disposition-selftest.*` → 0.

## Per-leg dispositions (live run, `observed_at 2026-10-20T15:21:25Z`)

Every row: `pinned.status=verified`, `head.status=present`, `result_reuse=not_established`,
`reason=null`. `head present` means only that the path exists as a blob at HEAD; it is not
a pin match (`tools/pin-disposition.py:42-43`). Worktree sha256 independently recomputed
with `sha256sum` for all six paths and matched the JSON exactly.

| Leg | Repo / path | Pinned commit | HEAD commit | HEAD blob = pin? | Worktree sha256 (12) | content_status |
|---|---|---|---|---|---|---|
| js-kimi-census | kumitate `scripts/kimi-census.mjs` | 175de6ba2e9e | 1770305fae20 | no (5e8d59132406) | 5e8d59132406 | changed |
| bash-surface-census | kagi `corpus/surface-census.sh` | fecee8743e52 | c2cab35bc92e | **yes** (275d8294a94e) | 275d8294a94e | unchanged |
| bash-tsukuroi-census | tsukuroi `tools/tsukuroi-census.sh` | 165307fe4746 | 6923fe0bd3ad | no (d17d32a35946) | d17d32a35946 | changed |
| bash-mado-verify | mado `tools/mado-verify.sh` | eead56b20ad2 | 0ab1ccccaac5 | no (fba82a662795) | fba82a662795 | changed |
| bash-checklist-run | kagi `corpus/checklist-run.sh` | fecee8743e52 | c2cab35bc92e | **yes** (7e5ec98b9e1d) | 7e5ec98b9e1d | unchanged |
| js-claims-check | kumitate `scripts/claims-check.mjs` | 175de6ba2e9e | 1770305fae20 | **yes** (e9a21b441f12) | e9a21b441f12 | unchanged |

For the three `changed` legs the worktree bytes equal the HEAD blob (the divergence is
committed, not dirty). For the three `unchanged` legs the file survived later commits
unchanged, so the repo HEAD is past the pinned commit while the blob bytes still equal the
pin — HEAD drift and content drift are independent, exactly as the tool's docstring says.

### Drift against the round-13 recorded reading

Compared with `.ufo/evidence/round-13/pin-dispositions.json`:

- Counts are identical (3/3/0/0) — but the observation is **not** identical:
  - tsukuroi leg HEAD moved `9574a189a758` → `6923fe0bd3ad`;
  - mado leg HEAD moved `59cfbdc3ab5e` → `0ab1ccccaac5`, and mado's worktree pin bytes moved
    `037b05dcd3f8` → `fba82a662795` (still `changed` both times).
- So a rerun that reports only `unchanged3/changed3` hides two sibling movements. Calibration
  point for C1/C2: the per-leg digests and HEAD commits are the dated observation; the
  counts are not.

## Sibling HEAD / branch-tip facts (read-only, `git symbolic-ref -q HEAD` + `rev-parse`)

21 sibling repos. For attached HEAD the `HEAD == tip` equality holds by construction (HEAD
is a symref to that branch); the informative comparison is the four detached/jj cases.

| Repo | HEAD state | HEAD (12) | Branch tip used | HEAD == tip | Dirty lines | `.jj` |
|---|---|---|---|---|---|---|
| audio-shokunin | attached `refs/heads/main` | 0462a5440f23 | same | yes | – | no |
| chousa-shokunin | attached `refs/heads/master` | d730ae4c3398 | same | yes | – | no |
| game-dev-2d-shokunin | attached `refs/heads/main` | bce53b83a21e | same | yes | – | no |
| game-dev-3d-shokunin | attached `refs/heads/main` | 3118be0b18dd | same | yes | – | no |
| kagi-shokunin | attached `refs/heads/master` | c2cab35bc92e | same | yes | – | no |
| **kaidoku-shokunin** | **DETACHED** | 9011581d8452 | `main` 9011581d8452 | **yes** | 1 (untracked `.ufo/waves/round-18/`) | yes |
| kake-shokunin | attached `refs/heads/master` | 7c61c8cc791b | same | yes | – | no |
| **kama-shokunin** | **DETACHED** | cff9e62f05aa | `master` cff9e62f05aa | **yes** | 8 (5 modified tracked, 3 untracked) | yes |
| kasegi-shokunin | attached `refs/heads/master` | 922a4dde90b6 | same | yes | – | no |
| kengaku-shokunin | attached `refs/heads/master` | 6180e4fb92e9 | same | yes | – | no |
| kotoba-shokunin | attached `refs/heads/master` | c61a973b2e02 | same | yes | – | no |
| kotodama-shokunin | attached `refs/heads/main` | 4ad268365524 | same | yes | – | no |
| kumitate-shokunin | attached `refs/heads/master` | 1770305fae20 | same | yes | – | no |
| lore-shokunin | attached `refs/heads/main` | 01306d51252f | same | yes | – | no |
| mado-shokunin | attached `refs/heads/master` | 0ab1ccccaac5 | same | yes | – | yes |
| mori-shokunin | attached `refs/heads/master` | 24526ea9617c | same | yes | – | no |
| revenger-shokunin | attached `refs/heads/main` | cf02419276e5 | same | yes | – | no |
| souji-shokunin | attached `refs/heads/master` | fb23b122eb99 | same | yes | – | no |
| tabi-shokunin | attached `refs/heads/master` | 6c8e0ff9c882 | same | yes | – | no |
| **tameshi-shokunin** | **DETACHED** | 98bea7da5801 | `master` 98bea7da5801 | **yes** | 3 (untracked round-16/17 evidence+waves) | yes |
| tsukuroi-shokunin | attached `refs/heads/master` | 6923fe0bd3ad | same | yes | – | no |

Detached repos: **kaidoku, kama, tameshi** — three, each detached exactly at its local
branch tip (`main` for kaidoku, `master` for kama/tameshi); each is also
`merge-base --is-ancestor HEAD <default branch>` = true, i.e. not ahead of the branch.
No repo anywhere is detached away from its branch tip. Four repos carry `.jj`
(kaidoku, kama, mado, tameshi); three of those are detached and mado is attached, so
"jj layout ⇒ detached" does not hold universally — [INFERENCE] mado's HEAD is symref-attached
while its jj working copy sits at the same commit as `refs/heads/master`.

`kama` is the only scanned repo with **modified tracked files** while its HEAD equals the
branch tip, so "at branch tip" there does not mean "a fresh checkout runs what I read".

The probe's per-leg `head.commit` equals the actual repo HEAD for all six legs
(checked programmatically against the scan above), so the repo-identity guard
(`tools/pin-disposition.py:235`, `:412`) resolved each leg's own repo, including the
detached/jj ones, and did not borrow the fleet super-repo.

## C2 sub-claim check: "branch-tip resolution in tools/pin-disposition.py"

At `98bea7da`, `tools/pin-disposition.py` is **byte-identical to the round-13 measured
artifact**: worktree sha256 = HEAD blob sha256 = round-13 `expected.json` pin
`297253971dab3a55…`. It contains no branch-ref read at all — `grep -n
"symbolic-ref\|for-each-ref\|branch"` returns nothing; the only git plumbing is
`rev-parse --show-toplevel` (`:255`), `rev-parse --verify <commit>^{commit}` (`:280`) and
`rev-parse --verify … HEAD^{commit}` (`:318`). So at this rev the declared jj fix "branch-tip
resolution in tools/pin-disposition.py" is **not present in the file**, and the pre-existing
repo-identity guard is round-13 code. `.ufo/waves/round-17/staged/` does not exist at read
time, so if that fix is planned it has not been staged yet. [INFERENCE] it may be a wave-1
in-flight change; as of this reading it is unbacked at the tip.

Operationally this does not hurt the registered outcome: the tool reports the HEAD commit
and the HEAD blob, which is sufficient under detached HEAD — for all six legs the reported
HEAD commit equals the repo's real HEAD. But a claim that a *new* jj fix landed in this tool
would be false at `98bea7da`.

## Limits / unknowns

- `content_status` is raw bytes only; `not_compared` (emitted verbatim):
  mode/exec-bit, runner version and embedded defect specs, suite command and test harness,
  interpreter and toolchain versions, environment variables, dependency versions, fixture
  and companion files, timeouts. Every row carries `result_reuse=not_established`.
- The probe executes no sibling gate; nothing here says a recorded mutation result may be
  reused.
- Attached-HEAD `HEAD == tip` is structural, not measured; only the three detached repos
  required a real tip comparison.
- Lane worktree changed while I read (other seats, not this item): ` M .gitignore`,
  ` M .ufo/evidence/round-16/round-gate/runner-sha256.txt`, new
  `.ufo/evidence/round-15/attempt-4/` and `verification-4.json`. `pin-disposition.py` is
  read-only by design (docstring `:73-83`) and wrote nothing.

**Verdict: holds for the two registered commands at `98bea7da` (selftest 0 / PASS 18-18, live probe 0 / 6 legs 3-3-0, invalid input 2); partial on the declared C2 "branch-tip resolution in tools/pin-disposition.py" fix, which is absent at this rev.**
