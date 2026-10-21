# H02 DepthUnchanged — command D at lane tip (BUILD advisory wave, round 20 attempt 2)

Seat: `TameshiR20-3.H02DepthUnchanged` (scout, read-only). Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Scope: run command D (`SCORECARD.md:73`) at the current lane tip; report `recorded_cases` and `depth_score`; confirm no ninth recorded case is added by this round and no depth claim is made. No installs performed (tooling directive: nothing to record).

## Observed state (read-only)

- `git rev-parse --verify master` → `6fd220bce3705498d1d1054e99e3cae73c203751` ("round-20: freeze QUALITY20 receipt-window contract and staged instruments (attempt 2)"). `HEAD` = same commit, so the worktree is at the tip.
- `master^` → `c144dcd807166dfc275c1ac2936fd2fa4b678bda` — the contract's declared baseline. Confirmed.

## Command executed (exact, `REV=master`)

```sh
git show "$REV:tools/mutate-and-run.sh" | python3 -c 'import re,sys; n=len(re.findall(r"^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+",sys.stdin.read(),re.M)); print("recorded_cases="+str(n)+" depth_score="+str(min(10,n)))'
```

Run from `/tmp` via `git -C <lane>`; `git show` is pure object-DB read, no Git/JJ mutation, no lane write.

## Observed outputs

1. **At master tip (6fd220b):** `recorded_cases=8 depth_score=8`
2. **At baseline (master^ = c144dcd):** `recorded_cases=8 depth_score=8` → **delta 0**; depth_score equals the frozen header values (depth=8, calibration=8).
3. **The eight matched ledger lines** in the tip blob (verbatim):
   - `js-kimi-census` kumitate 8/10 · `bash-surface-census` kagi 8/10 · `bash-tsukuroi-census` 6/10 · `bash-mado-verify` 4/10 · `bash-checklist-run` kagi 7/15 · `js-claims-check` kumitate 7/10 · `js-round-gate` kumitate 5/10 · `js-sources-check` kumitate 5/10
   These are the historical six plus round-16's `js-round-gate` and round-18's `js-sources-check`. No ninth line, no new gate.
4. **Blob identity:** `rev-parse master:tools/mutate-and-run.sh` = `rev-parse master^:tools/mutate-and-run.sh` = `fd1a63a3493b5a2fb2723f2fb1baae9ee7480fba`; `sha256` of tip blob = worktree file = `d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b` — exactly the contract's classified historical instrument `witness-runner`. The runner bytes are themselves a classified historical instrument and are unchanged by this round.
5. **Tip commit contents:** `git diff-tree --name-status -r master` → six entries, all `A`, all under `.ufo/evidence/round-20/` (`c1-before.json`, `c1-before.stdout`, `contract.json`, `final/receipt-window-selftest.json`, `stage/measure.py`, `stage/receipt-window.py`). No `tools/`, `SKILL.md`, `SCORECARD.md`, `SHONEN.md`, or `corpus/` change at the tip.

## Findings

1. **Command D at tip: `recorded_cases=8 depth_score=8`.** Matches the frozen context (tied lowest owned axis depth=8, calibration=8) and SCORECARD round-18's 7→8 history.
2. **No ninth case added by this round** — confirmed three independent ways: (a) command D identical (8→8) at baseline and tip; (b) tip commit touches no file outside `.ufo/evidence/round-20/`; (c) runner blob `fd1a63a` byte-identical across baseline/tip/worktree with sha256 `d22c4025…` equal to the classified `witness-runner` historical instrument.
3. **No depth claim is made** — contract `.ufo/evidence/round-20/contract.json` declares one claim C1, axis `calibration`, unit "QUALITY20 recurrence closed", `before 0/6 → target 6/6`; its invariants explicitly bar promotion, bar numeric calibration increase (cap 8), and keep the 18 guard survivors open. The staged ruler `stage/measure.py` contains zero occurrences of `depth`, `recorded_cases`, or `mutate-and-run` (grep: no matches) — the round instruments the receipt-window recurrence only, never depth. The historical instrument shas are named individually in the contract (`96a68b60…`=round19-ruler-wave1, `8dfaa25a…`=witness-tool, `d22c4025…`=witness-runner, `7ca87a7c…`=round18-measure), consistent with the rider against a singular "frozen SHA".

## Agree/disagree with frozen facts

Agree on every point verified: master = 6fd220b; baseline = c144dcd; staged instrument shas present in contract (`f03ae7e9…` receipt-window, `f34dc233…` measure); the four historical shas as classified; staged bytes untouched by me.

## Defects

None in lane artifacts. One probe artifact of my own, recorded for honesty: a supplementary line-reprint that anchored the canonical regex with `$` returned 0 matches (the ledger lines carry trailing column text); the unanchored canonical regex from command D is correct and was used for all reported numbers.

## Verdict

H02 confirmed: depth unchanged at tip — `recorded_cases=8 depth_score=8`, 8→8 against baseline, no ninth case, no depth claim in the round-20 contract or its ruler.
