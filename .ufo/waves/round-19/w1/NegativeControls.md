author: TameshiR19-2.NegativeControls (critic, advisory, read-only)

# Negative controls — five one-change corruptions of the round-19 corrections

Scope: attack the *closure predicates* for C1 (five routed round-18
metadata/receipt defects, frozen population in
`.ufo/evidence/round-19/contract.json`, baseline
`7243e7f163f08978c8fd9b6c1ef67a2fefe7d190`). Each control is **one change** to
one artifact the correction touched, designed so that an audit which scores
"an erratum/receipt exists" on labels passes, while an audit that re-verifies
the claim's provenance must reopen the defect. No production edits made;
mutations ran only inside `/tmp` snapshots against the frozen ruler.

Method note (evidence): each mutation was applied to a snapshot of the
delivered tip `21e79329f8bdcf01a62be63b3e46db4a7de6b6f9` blobs and graded by
the lane's own frozen ruler
`python3 .ufo/evidence/round-19/measure.py --snapshot SNAPSHOT --check`.
Pristine tip gives `corrected=5, exit=0`; each mutated snapshot below also
gave `corrected=5, exit=0` — i.e. **the frozen ruler itself accepts all five
corruptions**. That makes these genuine label-blind spots: a predicate-only
audit cannot catch them; a failure-capable audit must run the falsifier.

| # | Frozen item / defect | One-change control | Observed under frozen ruler | Falsifier (why a real audit must fail it) | Minimal defensible acceptance |
|---|---|---|---|---|---|
| NC-1 | R18-1, `corpus/knowledge/guard-kill-closure.md` — stale `verified-at` PENDING | In Erratum R18-1, swap the cited effective receipt path `final/probes.stdout` → `c2-probes-v2-183f87b.txt`, keeping the quoted text `DEFECT_PROBES: open=0 closed=11 total=11` and revision `921ef80…` intact | R18-1 `corrected` (ruler checks only that `TOOLS18` appears and that the real probes row digests match — it never resolves the cited path) | `c2-probes-v2-183f87b.txt`'s own last lines read `DEFECT_PROBES: open=11 closed=0 total=11` — the cited receipt literally reports the opposite tally. Erratum quotes text the file does not contain. A receipt-bound audit opens the cited path and fails it | Erratum must name the exact committed path **and** the tally must be re-verifiable at that path: `tail` of the named file must equal the quoted verdict line, at the named revision `921ef8077440f90d092aab4b9fdc750a45de1224` |
| NC-2 | R18-2, S008 status in `corpus/knowledge/mutation-case-kumitate-sources-check.md` + `corpus/SOURCES.md` row | Change the S008 `opened` cell `2026-10-19` → `2026-10-21` (fabricated re-open date); `mined` and `used-by` stay correct | R18-2 `corrected` (ruler checks only cells 8=`mined`, 11 contains the entry path, 13-cell shape — dates are free fields) | The committed base row records `opened=2026-10-19`; no source re-open at 2026-10-21 is documented for S008 (unlike S049, whose round-19 re-open IS disclosed in `corpus/lessons/round-19.md` Gate). Unfounded date mutation = silent provenance edit, exactly the defect class being repaired | Correction must leave every *other* cell byte-identical to the base `4b7c682` row unless the diff is itself disclosed; the erratum's factual claims must be re-derivable from `git show 4b7c682…:corpus/SOURCES.md` |
| NC-3 | R18-3, falsifier arithmetic in `corpus/lessons/round-18.md:79` erratum | In Erratum R18-3's counting command, change the right-hand bound `4b7c6823a462f5ea2eafcb262275300a545f3ed7` → `HEAD`; keep the "five deleted table lines" claim and the `25 5` receipt | R18-3 `corrected` (ruler greps the erratum for five IDs and regexes `25\s+5` in `sources-diff.txt` — the stated command is unexamined text) | The receipt `sources-diff.txt` is bound to `183f87b…4b7c682`; a command with `HEAD` re-measures a moving target (observed: `git diff --numstat 183f87b 4acdeac` and `…9ee1c80` also happen to give 25/5 today, but any later SOURCES edit silently shifts it). An unfrozen bound makes the falsifier non-reproducible — the same "unbound revision" defect the erratum exists to fix | The erratum's stated command must be byte-for-byte re-runnable at full-length frozen revisions, and its output must byte-match the committed receipt `sources-diff.txt` (verified: `25\t5\tcorpus/SOURCES.md`) |
| NC-4 | R18-4, `bash-witness-selftest` failed-invocation row → `.ufo/evidence/round-19/bash-witness-selftest-complete.json` | Set `runner_sha256` to `1111…` (all ones) inside the new receipt; argv/exit/digest chain untouched | R18-4 `corrected` (`receipt()` validates argv, revision, exit, stream paths, stream digests, empty stderr — `tool_sha256`/`runner_sha256`/`recorded_at` are unconstrained provenance fields) | `tool_sha256` is independently checkable: `git show 4b7c682…:tools/bash-witness-study.py | sha256sum` = `8dfaa25a…32e3a12` (matches). A falsified `runner_sha256` declares the scratch runner was a specific blob that never existed — provenance fabrication inside the receipt that "fixes" a provenance defect | Every declared hash in the receipt must be re-derivable from committed bytes at the receipt's own `revision`; unverifiable provenance fields (runner identity, cwd kind, recorded_at) must be either verifiable or explicitly labelled unverifiable |
| NC-5 | R18-5, missing 60/60 receipt at `4b7c682` → `.ufo/evidence/round-19/round18-final-measure.json` | Backdate `recorded_at` `2026-10-21T05:28:25Z` → `2026-10-21T02:00:00Z` — *before* the contract-freeze commit `78b99dd` (`2026-10-21T02:28:10-03:00` = 05:28:10 UTC) | R18-5 `corrected` (`receipt()` ignores `recorded_at` entirely) | Ordering contradiction: the receipt claims it ran 3h28m before the population/contract that created it existed, and before the sibling witness failure (`05:28:42Z`). A timestamp audit or causal-order check fails it; a digest-only audit cannot see it | `recorded_at` must post-date the freeze commit `78b99ddcbf46f06246b978c8f5d4b6720dc5f59e`; the late-repair disclosure in the erratum ("does not claim the receipt existed in round 18") is itself only credible if the timestamp ordering is consistent |

## Cross-cutting finding

The frozen ruler `measure.py` is a **token-plus-digest** predicate: it
validates the digest chain *inside* receipts and required substrings *inside*
errata, but it never resolves a cited path, never re-derives a declared hash
against the named revision, never checks a stated command for a frozen bound,
and never checks timestamp ordering. All five controls pass it. Therefore the
C1 closure predicate cannot rest on `measure.py --check` alone; the
"failure-capable audit" the claim demands must add a provenance pass:

1. every path a correction cites must be opened and its relevant line matched;
2. every declared `*_sha256` must be re-derived from `git show REV:path`;
3. every stated counting/diff command must carry full-length frozen revisions;
4. every `recorded_at` must be ≥ the freeze commit timestamp.

These are the smallest additions that close all five label-blind spots
without widening the claim.

## Sources / commands run (all read-only; mutations in /tmp only)

- `corpus/lessons/round-18-verifier-spotcheck.md` §5 — the five routed defects (authoritative defect text).
- `git show 21e7932 -- <files>` — the delivered corrections (Errata R18-1…R18-5).
- `.ufo/evidence/round-19/contract.json` — frozen population, invariants, acceptance `corrected=5 failed=0`.
- `.ufo/evidence/round-19/measure.py` — the frozen ruler; predicates quoted above.
- `.ufo/evidence/round-18/final/checks.json` — `probes` argv `--rev 921ef80…` exit 0; `bash-witness-selftest` argv `--selftest` exit 64.
- `git show 4b7c682…:tools/bash-witness-study.py | sha256sum` → `8dfaa25a…32e3a12` (matches receipt `tool_sha256`).
- `tail -3 .ufo/evidence/round-18/c2-probes-v2-183f87b.txt` → `DEFECT_PROBES: open=11 closed=0 total=11` (NC-1 falsifier fact).
- `git log -1 --format=%cI 78b99dd` → `2026-10-21T02:28:10-03:00` (NC-5 ordering bound).
- `python3 .ufo/evidence/round-19/measure.py --snapshot <mutated> --check` → `corrected=5, exit 0` for all five mutations; pristine tip `21e7932` → `corrected=5, exit 0`; baseline-style empty artifacts → `open` (ruler itself is not blind, just shallow).

No tools installed; no production files, refs, or receipts modified.
