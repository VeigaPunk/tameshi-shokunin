# T58W1Verify03 — row verification

Base: `2a32aa8228d5f86a85c81a923a3148bf792a9538`.

## Method and retained evidence

Created `/fast/scratch/hyaku/tameshi-r58/T58W1Verify03/clone` using `git clone --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin ...`, detached it at the required base, and confirmed `git rev-parse --show-toplevel` printed the clone directory. Assignment text was read from the frozen round-58 defects record. Ran `grep -nE 'drift-pins|cross-domain|## Gate|rejected candidates|case 10|receipt-recency-by-last-touch|freeze-stamped|control receipts'` over the round-51 spot-check and kill-rate ledger; this found the four lines below. Ran a second recursive grep over base `corpus/lessons` and `corpus/knowledge` for the relevant routing/receipt phrases; it surfaced no completion of the R51.5/R51.6/R51.8 tasks. `git log --format='%H %s' -- corpus/knowledge/fleet-kill-rate-ledger.md` identified `bcba8924894216268afc4171f06eb8c28e912b46` as the round-52 ledger change containing R51.7's supersession.

- **R51.5 — open; proposed open.** `corpus/lessons/round-51-verifier-spotcheck.md:130` says “Cross-domain routing owed to kagi” and instructs filing the `drift-pins.sh --selftest` finding in the next report. The base grep shows it remains stated as an owed action; the recursive search did not find a routed report completion. No round-58 fix commit intent is established, so `commit` is null.
- **R51.6 — open; proposed open.** `corpus/lessons/round-51-verifier-spotcheck.md:131` explicitly asks for rejected candidates with reasons in the round lesson's `## Gate`. The base search found this recorded as an owed correction, not evidence of completion. `commit` null.
- **R51.7 — fixed.** `corpus/knowledge/fleet-kill-rate-ledger.md:441` states that case 10 measured drift-pins and supersedes the §3 cell that said “unmeasured by sweep.” `git log` reports introducing ledger change `bcba8924894216268afc4171f06eb8c28e912b46` (round 52); cited in JSON. This resolution excerpt includes the key `case 10` and is not an ACK_WORD claim.
- **R51.8 — open; proposed open.** `corpus/lessons/round-51-verifier-spotcheck.md:133` labels the freeze-stamped control receipt issue and says “Not yet shown able to fail.” Recursive grep found the observation, not a later resolution/failure demonstration. `commit` null.

Rows and excerpts are in `T58W1Verify03.json`. No lane content was edited. No checks/builds/tests/formatters were run. Scratch clone and scratch directory removed before return. No tools installed.
