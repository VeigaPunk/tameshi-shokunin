# ReviewAmend2Facts — fact-check of `.ufo/evidence/round-32/v2/contract-amendment-2.json` (data disclosure)

Seat: `ReviewAmend2Facts` (TameshiR32, wave 2, 2026-10-23). Leaf; read-only against the record (lane reads via `git log`/`git show`/file reads only; no counter, tool, gate or selftest executed; nothing written outside this report and my scratch dir; no installs made; no processes left running).

Method note: no LSP device is exposed in this session (not in the tool inventory), so all caller/definition checks are text reads plus git reads; that unavailability is recorded rather than presented as semantic proof. The `grep` tool timed out (30 s) scanning all of `/fast/scratch/hyaku/tameshi-r32-seats/`; the fallback was a read-only `grep -rlF --binary-files=without-match --exclude-dir=.git` over the same tree (completed in ~63 s and ~77 s for the two scans).

## Verdicts

| # | Statement in `data_disclosure` / item | Verdict |
|---|---|---|
| (a) | "No v2 counter run has been made on any real tool bytes before this amendment." | **SUPPORTED** (absence-of-receipt evidence; see caveat) |
| (b) | "v1 runs on the real tool bytes exist: DeterminismProbe's … v1 stopped being the claim's rule at amendment 1, before those runs were known to the L1." | **SUPPORTED** in every checkable part; the "known to the L1" clause is consistent with the record but not independently provable from it |
| (c) | Commit order c3181497 -> e9f3b957 -> b50a18f0 -> 528f8dee -> a4f718138bdad20de741faeca57891645e5a64d9 | **VERIFIED exactly** (linear parent chain, timestamps strictly increasing) |
| (d) | Dev-sweep disclosure (devsweep.py, "120 seeds: 468 distinct bodies, 0 misses", "200 seeds receipt devsweep-200.stdout") | **SUPPORTED**; both body counts reproduced exactly from the public counter; one nuance: the 120-seed run itself has no receipt |
| — | Line 4: pinned-identity change after v1-subset data (the §9 ruling itself is the L1's judgment) | **SUPPORTED as a factual statement**; the §9 ruling is out of my scope and not judged |

## (a) No v2 counter run on real tool bytes before 528f8dee — evidence

528f8dee was committed 2026-10-23T08:01:24-03:00. Evidence class: every v2-counter run prints a `C1_R32V2:` summary line and `HELDOUT` lines (counter source lines 44, 294–318, 397), so run receipts are findable by literal string.

- `C1_R32V2:` in `.ufo/waves/round-32/w1/` (all 35 reports): **0 matches**.
- `C1_R32V2:` in `.ufo/evidence/round-32/`: matches only in the counter's own source (`c1-measure-v2.py` docstring/print lines) and the item text inside `w2-items.json`. No receipt anywhere in the lane evidence tree.
- `C1_R32V2:` across all seat scratch dirs (read-only scan): earliest hit 07:55:07 — `ReviewCounter/clone/.ufo/evidence/round-32/v2/c1-measure-v2.py` + `contract-amendment-1.json`: the string is **source text**, files checked out from b50a18f0; no run output file in that seat's scratch. Every other hit is >= 08:22:57 (wave-2 clones of post-amendment revisions) or MutCounterV2's own probe outputs at 08:27:00–08:29:09.
- `HELDOUT ` across all seat scratch dirs: same shape — source files and MutCounterV2 probe outputs, all >= 08:27:00. No pre-08:01:24 output anywhere.
- MutCounterV2's post-amendment probe runs are **not** the frozen counter on real bytes: `MutCounterV2/probes/base/v2/c1-measure-v2.py` pins `TOOL_SHA256 = '57caea6660ba2fdd4dab02add9452e5126fc3a28c72a30c26f254002033f697d'` (a fixture sha), its summary names sandbox rev `3b8bacf…ea7`, and its COPY lines end `TALLY_AUDIT: FAIL always-fail fixture`. The frozen counter's sha256 is `1ab9e9cf8e408f6230110ac42495da2b9c3f51236fe3a32754bd23524f7f7c94` (worktree = blob at 528f8dee, verified identical).
- The v2 counter first exists at b50a18f0 (07:54:42): `git log -- .ufo/evidence/round-32/v2/` lists exactly b50a18f0 and 528f8dee. `.ufo/evidence/round-32/heldout/` has **no commits and is absent from the worktree** — consistent with "the held-out set is written only after this amendment".

Caveat (residual): the claim is supported by absence of receipts. A run that crashed before printing a receipt and left no artifacts cannot be excluded by this method.

## (b) DeterminismProbe's v1 runs on real tool bytes: shas and timing — evidence

Source: `.ufo/waves/round-32/w1/DeterminismProbe.md` §1a table + §5 index; dates from receipt mtimes in `/fast/scratch/hyaku/tameshi-r32-seats/DeterminismProbe/out/`.

Tool shas the v1 counter (`c1-measure.py`) was run against, per §1a:

- `efec2ece…b8db6` — always-FAIL control (clone d747b80), §2a/2b/2d;
- `ec2a1ef1…40e3` — path-echoing control variant (bb423ff), §2c;
- `ad7be824…2010` — seed-keyed single-copy probe (9a3fc37), §3e;
- **`ac38a1ac…c819c` — real capability tool** (read-only copy, clone b80e78b), §3 sweep/3b/3c/3d;
- **`158202f8…a356a` — real capability tool, newer bytes** (read-only copy, clone 556d1ff), §3a re-verification.

Timing (mtime of the receipts, all 2026-10-23 -03:00): controls 07:43:17–07:44:47; real-tool runs on `ac38a1ac` (`real-seed2a-1` … `sweep-0b00`, `sweep-summary`) 07:45:29–07:54:08; re-verification on `158202f8` (`re-00ff`, `re-0900`, `re-2a`) 07:54:45–07:55:04. Amendment-1 (b50a18f0) was committed 07:54:42 — between the two groups; `158202f8` is exactly the tool blob committed at b50a18f0 (`git show b50a18f0:tools/tally-audit.py | sha256sum`). Amendment-2 (08:01:24) postdates every run. The amendment's `reason` figures match the report: 16 of 72 gH05 (drop,dup) pairs escape; "about 2 seeds in 9 print false" vs the report's 23.6% over 2000 seeds (2/9 = 22.2%).

Calibration: "before those runs were known to the L1" — the `ac38a1ac` sweep completed 34 s before amendment-1 was committed; whether the L1 had read it by then is not decidable from artifacts (the report file was committed only at a4f71813 08:01:58, yet amendment-2 already cites it at 08:01:24, and the report records an L1 stop request after its last run at 07:55:04). Consistent with the record; not independently provable.

## (c) Commit order — evidence

`git -C tameshi-shokunin log --format="%h parent=%p %cI %s" e24688b2…a4f71813`:

```
a4f7181 parent=528f8de 2026-10-23T08:01:58-03:00 round-32: content revision …
528f8de parent=b50a18f 2026-10-23T08:01:24-03:00 round-32: amendment 2 before any v2 run …
b50a18f parent=e9f3b95 2026-10-23T07:54:42-03:00 round-32: C1 re-designed before data …
e9f3b95 parent=c318149 2026-10-23T07:42:18-03:00 round-32: wave-1 spec, generator and dispatch record …
c318149 parent=e24688b 2026-10-23T07:38:24-03:00 round-32: freeze — C1 counter + contract …
```

Linear chain, order and times exactly as claimed. Tool blob identity: `b50a18f0:tools/tally-audit.py` = `158202f8bc85…a356a`; `528f8dee:` = `9639c458002c…99ef` = the amendment's `new_TOOL_SHA256`; unchanged at a4f71813.

## (d) Dev sweep receipts — evidence

`.ufo/evidence/round-32/v2/dev/` contains exactly: `devsweep.py` (mtime 07:58), `devsweep-200.exit` ("0"), `devsweep-200.stdout` ("`DEVSWEEP bodies=688 kill=282 accept=406 misses=0`"), all committed at 528f8dee (`git ls-tree -r 528f8dee -- .ufo/evidence/round-32/v2/`). `devsweep.py`'s docstring states it ran before the amendment-2 freeze and is disclosed — consistent with its mtimes (07:58–08:00, before 08:01:24).

I reproduced the stated counts read-only by importing the public v1 counter module and calling its family builders against the pinned runner blob (no counter execution, no tool runs): **120 seeds -> 468 distinct bodies** (kill 222 / accept 246); **200 seeds -> 688 bodies** (kill 282 / accept 406). The `devsweep-200.stdout` receipt matches the 200-seed recomputation field-for-field, and the amendment's "468 distinct bodies" matches the 120-seed recomputation exactly.

Nuances: (i) no receipt exists for the 120-seed run itself — its "0 misses" follows only from the 200-seed superset receipt (468 ⊂ 688 bodies, seeds 0..119 ⊂ 0..199) plus the plausible-but-unreceipted assumption both runs used the same working-tree tool bytes; (ii) the receipts bind no timestamp or tool sha — that the sweep ran on `9639c458` bytes is inferred from mtimes (after `9639c458` was first observed ~07:55, before the 08:01:24 commit), not proven by the receipts.

## Line 4 — pinned identity changed after v1-subset data

Factually supported: `TOOL_SHA256` moved `158202f8` -> `9639c458` between b50a18f0 and 528f8dee while v1-subset data predates 528f8dee (DeterminismProbe's real-tool v1 runs 07:45–07:55; wave-1 CriticC1 allowlist; dev sweep 07:58–08:00), and the held-out set did not exist yet (empty/uncommitted `heldout/`, no pre-08:22 `HELDOUT` receipts). Whether this is or is not a §9 rule change is the L1's judgment; I make no ruling on it.

## Residual risk

- (a) rests on absence of receipts; unlogged or crashed-then-wiped runs cannot be excluded.
- Wave-2 seats run *modified* v2 counters on fixture bytes in their sandboxes (MutCounterV2 confirmed). None touches the frozen counter (`1ab9e9cf…`) on real tool bytes, but downstream reviewers must keep probe counters (patched `TOOL_SHA256`) distinct from the frozen one when weighing "first full v2 run" claims.
- The held-out half of the predicate (>= 6 valid held-out must-kill / must-accept, written after the freeze) is not yet checkable against the record — `heldout/` is still empty and uncommitted at review time.

## Verification gaps

- No LSP device available in this session; all checks are text/git evidence.
- I did not execute the counter or the tool (bounds); counts were recomputed by module import only.
- The "known to the L1" clause (b) and the §9 judgment (line 4) are knowledge/judgment claims not decidable from artifacts.

Report: .ufo/waves/round-32/w2/ReviewAmend2Facts.md
