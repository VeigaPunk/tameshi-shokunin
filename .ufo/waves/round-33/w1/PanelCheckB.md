# PanelCheckB — independent repeat of PanelCheckA (seed-independence of the public panel verdict)

Seat: tameshi-r33-w1-PanelCheckB-4
Date: 2026-10-23
Role: reviewer (operability axis)

## Verdict

No finding. The round-32 v1 counter's public-panel verdict is seed-independent for both frozen
tools: under four distinct seeds, both the v1 tool (`tools/tally-audit.py` at f6d8a891, sha256
9639c458002ce2f954addbe047427010ae011353e073b293396bec800fa699ef) and the v2 tool
(`tools/tally-audit-v2.py` bytes, sha256 9dbbce62aeaeecbacfa1b82e15b61afcb4580e3920a0b827ae038fa4c06f33a4)
score kill=18/18 accept=8/8 other=0, runner_sha_ok=1, tool_present=1, C1_R32_PASS=true, exit 0.
Seeds are my choice and differ from PanelCheckA's (`0123456789abcdef` / random): I used
1111111111111111, 2222222222222222 (v1) and 3333333333333333, 4444444444444444 (v2). The four
generated family sets differ across seeds (verified: different gT08 arm values, gN05/gH03/gH04/
gH05/gN01/gD01 parameter draws), so the runs exercised genuinely different panels. No correction
needed; no production changes; no tool installs performed.

## Setup (within my scratch only)

- Scratch: `/fast/scratch/hyaku/tameshi-r33-seats/tameshi-r33-w1-PanelCheckB-4/`
- Clone: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone --no-checkout
  /home/vgpnk/Projects/shokunin/tameshi-shokunin <scratch>/clone`
- Checkout: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C <scratch>/clone checkout
  --detach f6d8a891f1d966c5c3cdda385090da3a6e804675` → "HEAD is now at f6d8a89 round-33:
  freeze C1 (tally-audit-v2 + counter v3, controls-gated) and C2 (S055 versioned-pin repair)
  before any data seat" (exit 0).
- Runner pin at rev: `git show f6d8a891:tools/mutate-and-run.sh | sha256sum` →
  `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` (matches frozen pin).

### Why a synthetic commit for the v2 runs

The round-32 v1 counter reads the tool from `git show rev:tools/tally-audit.py` only (the v2
tool lives at the separate path `tools/tally-audit-v2.py`). To score the v2 bytes with that
counter, I created one synthetic commit in my scratch clone that replaces
`tools/tally-audit.py` with the v2 tool bytes (copied from the lane's
`tools/tally-audit-v2.py`; the runner file untouched):

- Commit: `b1fe86711d98099a810d8c61485c2197799eb1ee` ("PanelCheckB synthetic: v2 tool bytes at
  v1 counter path"), parent f6d8a891. The counter later confirmed the executed tool blob sha
  `9dbbce62…` (`w3/tool/tally-audit.py`). v1 runs use rev f6d8a891 directly (tool blob
  `9639c458…` at `w1/tool/tally-audit.py`).

## Runs (receipt discipline: `cmd; echo $? > file`)

Command per run:
`python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py
--lane <scratch>/clone --rev REV --work <scratch>/wN --seed SEED > <scratch>/<tag>.out
2> <scratch>/<tag>.err; echo $? > <scratch>/<tag>.exit`
(script `<scratch>/run-panel.sh`; all runs completed in 2m43s, wrapper exit 0; stderr empty for
all four runs).

| Run | Tool (rev) | Seed | Summary line | Exit |
|---|---|---|---|---|
| v1-s1 | v1 (f6d8a891) | 1111111111111111 | `C1_R32: kill=18/18 accept=8/8 other=0 runner_sha_ok=1 tool_present=1 seed=1111111111111111 rev=f6d8a891f1d966c5c3cdda385090da3a6e804675 C1_R32_PASS=true` | 0 |
| v1-s2 | v1 (f6d8a891) | 2222222222222222 | `C1_R32: kill=18/18 accept=8/8 other=0 runner_sha_ok=1 tool_present=1 seed=2222222222222222 rev=f6d8a891f1d966c5c3cdda385090da3a6e804675 C1_R32_PASS=true` | 0 |
| v2-s1 | v2 (b1fe867) | 3333333333333333 | `C1_R32: kill=18/18 accept=8/8 other=0 runner_sha_ok=1 tool_present=1 seed=3333333333333333 rev=b1fe86711d98099a810d8c61485c2197799eb1ee C1_R32_PASS=true` | 0 |
| v2-s2 | v2 (b1fe867) | 4444444444444444 | `C1_R32: kill=18/18 accept=8/8 other=0 runner_sha_ok=1 tool_present=1 seed=4444444444444444 rev=b1fe86711d98099a810d8c61485c2197799eb1ee C1_R32_PASS=true` | 0 |

Each run printed 26 COPY lines (18 kill + 8 accept) with zero `other` outcomes. Exit files:
`v1-s1.exit`=0, `v1-s2.exit`=0, `v2-s1.exit`=0, `v2-s2.exit`=0. Receipts on disk in my
scratch: `v1-s1.out/.err/.exit`, `v1-s2.out/.err/.exit`, `v2-s1.out/.err/.exit`,
`v2-s2.out/.err/.exit`, plus work dirs `w1..w4`.

### Seed diversity evidence (generated kill families, run 1 vs run 2)

- v1 run1: `gT08(arm=5)`, `gN05(<= nlegs - 1)`, `gH03(form=1)`, `gH04(:)`, `gH05(drop=4,dup=6)`, `gN01(vector=0)`, `gN02(or)`, `gN03(split)`, `gD01(drop=st_citecheck,dup=st_tsu)`
- v1 run2: `gT08(arm=48)`, `gN05(< nlegs + 0)`, `gH03(form=2)`, `gH04(true)`, `gH05(drop=8,dup=5)`, `gN01(vector=1)`, `gN02(or)`, `gN03(or)`, `gD01(drop=st_roundgate,dup=st_kagi)`
- v2 run1: `gT08(arm=34)`, `gN05(< nlegs)`, `gH03(form=1)`, `gH04(rc=$?)`, `gH05(drop=1,dup=8)`, `gN01(vector=1)`, `gN02(or)`, `gN03(or)`, `gD01(drop=st_js,dup=st_citecheck)`
- v2 run2: `gT08(arm=108)`, `gN05(< nlegs)`, `gH03(form=2)`, `gH04(rc=$?)`, `gH05(drop=0,dup=5)`, `gN01(vector=2)`, `gN02(or)`, `gN03(or)`, `gD01(drop=st_mado,dup=st_sourcescheck)`

## Conclusion

The panel verdict is seed-independent: four different panels, identical verdicts. Both the v1
tool and the v2 tool still meet the live public panel (18/18 kill, 8/8 accept), consistent with
the expected calibration. No deviation found; smallest safe correction: none.

Residual risk / verification gap: this check covers the public panel only (round-32 v1 counter
families). It says nothing about the round-33 sealed held-out set, which is wave-2 data; the
sealed set and the round-33 v3 counter are out of this item's scope. The v1-tool scoring is
against the panel as defined by the round-32 v1 counter, not the round-32 held-out seal (which
defeated v1 by design).
