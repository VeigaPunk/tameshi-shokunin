The gate does not treat the clone path and the live lane path as equal: `command-binding.py` compares cwd as an exact string, with no realpath or abspath step. But the actual replay's cwd check is self-referential, and 2 of the 43 receipts that report the clone cwd got part of their result from the live fleet. That makes "43/43 in an isolated clone at 496d212" (SCORECARD and the knowledge entry) an overclaim. Both problems are fixable, and neither is a reason for the judge to reject the gate itself.

I wrote no files, including `.ufo/waves/round-23/w2/CwdDeclared.md`, because this wave forbids report writes. I ran no gate, test, build or formatter, and installed nothing. The only commands were read-only inspections (`git show`, `sha256sum`, JSON reads). The gate hash at the frozen revision 336565f is identical to the one at 496d212 (`d533dc…`).

**1. The cwd check on the real replay can never fail. Impacted axes: calibration, provenance honesty.**
- **Counterexample:** in `replay.py` lines 62 and 66, the bundle cwd and every receipt cwd are both written from the same variable, `str(clone)`. So `CWD_MISMATCH` cannot fire on that population, and the 43/43 cwd agreement carries no information.
- **Evidence:**
  - All 43 receipts carry the same cwd, `/tmp/tameshi-r23-replay-naxu6fzi/fleet/tameshi-shokunin`.
  - That directory no longer exists, so the value can't be checked afterwards.
  - Neither `contract.json` nor `requirements.json` declares a cwd. `expected.json` only pins the digest of the bundle the producer wrote.
  - The `mkdtemp` path can't be known before execution. That conflicts with workflow step 1 in `required-command-binding.md` ("freeze … before executing") and with its line 34 ("a relocated replay requires its own exact cwd contract"). No such contract exists for the replay.
  - Only the synthetic fixtures exercise a cwd mismatch: `/fixture/repo` versus `/other` and `/elsewhere`.
- **Smallest safe correction:** state that the replay's cwd field is a producer-declared clone path that agrees with itself and was not checked against any frozen value. Alternatively, freeze an execution root before running and record the clone under it.

**2. Clone-cwd receipts include live-fleet reads. Impacted axes: provenance honesty, deterministic replay.**
- **Counterexample, `pin-disposition-read`:** its argv includes `--root /home/vgpnk/Projects/shokunin`, and its output shows the manifest came from the clone while the root was the live fleet. The runner flagged it with `non_hermetic_argv`, and the row is marked `external: true`.
- **Counterexample, `verify-round15`:** `verify.py` lines 835–837 hard-code the live census script `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`. That validates the live lane's `corpus/SOURCES.md`, not the clone's. The absolute path sits inside the script, not the argv, so the runner recorded no `non_hermetic_argv` for it.
- **Where the signal is lost:** the projection in `replay.py` lines 67–71 drops `external` and `non_hermetic_argv`. Both receipts therefore claim cwd = clone and revision 496d212, and the gate returns a clean `0/[]`.
- **Timing (inference):** live HEAD during the replay window (14:42–14:44Z) was probably 496d212, committed at 11:41:18 -03:00, with the next commit at 11:46:12. So the bytes probably matched, but the state of the live working tree at that moment was not observed.
- **Smallest safe correction:** carry an `external` or live-read marker into those receipts, or report the result as 41 hermetic plus 2 live-dependent. Don't describe all 43 as isolated-clone results.

**3. `replay.py` has its own clone logic that skips registry-check's realpath handling. Impacted axes: deterministic replay; it also duplicates an existing authority.**
- **Counterexample:** `replay.py` re-implements the clone setup that `registry-check.py` already provides (`clone_lane_at_rev`, lines 757–783). Where `registry-check.py` uses realpath for the fleet root and sibling identity (lines 762–763, 780, 1907), `replay.py` compares siblings with plain string equality (line 52) and passes the raw `args.repo.parent` as the fleet root (line 60).
- **Effect:** run with a non-canonical `--repo` such as `/home/vgpnk/Projects/shokunin/kagi-shokunin/../tameshi-shokunin`, the hermeticity check `_argv_outside_fleet` would miss live paths under `/home/vgpnk/Projects/shokunin/`. That run would not mark `non_hermetic_argv`, and a row not declared external would no longer be stopped. The actual A run used the canonical absolute path, so its receipts are not affected; this is latent.
- **Smallest safe correction:** compute the fleet root as `os.path.dirname(os.path.realpath(args.repo))`, or reuse `clone_lane_at_rev`.

**No defect found:**
- The gate never treats the clone and the lane as the same place. A bundle declaring the live lane path with a receipt at the clone path returns `CWD_MISMATCH`.
- No receipt relabels the clone as the live lane. The gate-invocation receipts (`replay-gate-A.json`, `c1-after-A.json`) correctly record the live lane cwd, because that is where the gate actually ran.
- A forged receipt that agrees with itself and declares the live path for a clone run would still pass. That limit is already disclosed as "no producer authentication".
- Historical R17-CMD-BIND stays open; none of this closes it.
