# ReviewQ140 — hand-check quarantined tameshi S140 (F5 env-diff receipt row)

Verdict: **REFUSE — payload-absent stands.** Neither the register's quoted span nor
the row's own recheck output can be presented from the cited source, companion
artifacts, or the lane's git history. The evidence chain is volatile (run receipts
in `/tmp`, never committed) and the quoted span is mis-bound to a sibling row's run.

## The row and the quote

- Row under review: `/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md:38`
  (staged id S140): "tameshi's hermetic-environment differential receipt over the
  fleet gate selftests — .ufo/evidence/round-35 (contract), /tmp/r4-env-diff.json
  (receipt), tools/env-diff.py", repository
  `https://github.com/VeigaPunk/tameshi-shokunin`, recheck expects
  `ENVDIFF: classified=4/4`.
- Register quarantine:
  `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md:226`
  — `tameshi | round5 | S140 | payload-absent | https://github.com/VeigaPunk/tameshi-shokunin | ENVDIFF: classified=5/6 out=/tmp/r5-env-diff.json`
  ("cited source, companion URLs and local artifacts were all checked; the quote is
  in none of them").

## What I fetched and checked

1. **Cited source is reachable and is this lane.** `git ls-remote origin HEAD` →
   `5641ed84c8dc148c34c8dd83f062279ddf06b4af`, equal to lane HEAD — the remote fetch
   succeeded, so this is `payload-absent`, not `unreachable`.
2. **Quote absent from the whole cited repository at all revisions.**
   `git log -S 'classified=5/6' --all` → no commits; `git log -S 'r5-env-diff' --all`
   → no commits; `git log -S 'ENVDIFF' HEAD` → only `c318149, 67c0e01, 2da841b,
   87eb64e, c111dab` (the string's introduction via `tools/registry.json` /
   `tools/env-diff.py`, which contain `ENVDIFF_SELFTEST`/`ENVDIFF_CASE` format
   strings, not the run line). Working-tree grep for `classified=5/6`,
   `r5-env-diff`, `r4-env-diff` → zero hits.
3. **Companion receipt artifacts are gone.** `/tmp/r4-env-diff.json`,
   `/tmp/r5-env-diff.json` and `/tmp/r5-env-contract.json` do not exist
   (`ls` → No such file); `find /tmp -name '*env-diff*'` → nothing. No
   `env-diff`/`surfaces` receipt anywhere under `.ufo/evidence/`
   (`find .ufo -name '*env*'` and `grep -rln '"surfaces"\|classified='` → unrelated
   hits only). `lanes/tameshi/round4/` and `round5/` in shokuknow contain no
   `evidence/` receipt files.
4. **The cited contract cannot produce the quoted output.** The row's anchor cites
   `.ufo/evidence/round-35 (contract)` and "a contract carrying a `surfaces` list"
   is required by the instrument, but `.ufo/evidence/round-35/contract.json`
   (at 31687496 and HEAD) is a claims/axis contract with no `surfaces` key — the
   r4/r5 runs used a derived, unpersisted `/tmp` contract. The run is not
   re-derivable from the cited materials.
5. **The quoted span is mis-bound.** The register's `ENVDIFF: classified=5/6
   out=/tmp/r5-env-diff.json` is the S144 (six-gate) run's summary line
   (`lanes/tameshi/round5/SOURCES-PROPOSED.md:31`,
   `lanes/tameshi/round5/KNOWLEDGE-PROPOSED.md:40`), while the merged S140 row at
   `SOURCES.append.md:38` describes the four-gate run expecting
   `ENVDIFF: classified=4/4`. Row and quote disagree with each other.
6. **Instrument pin checks out but cannot rescue the row.**
   `sha256sum tools/env-diff.py` → `e8b47ab7cf2323764d9e9d3519352cd75e1abda4d5e98e7df602dc23bc099ead`,
   matching the row's `e8b47ab7cf232376…` prefix; `tools/env-diff.py:244` does
   print `ENVDIFF: classified={done}/{len(rows)} out={a.out}`. The instrument is
   real; the quoted *run output* is unpresentable.
7. **Dangling `used-by`.** Row 38's last cell names
   `corpus/knowledge/r4-env-diff-measured.md`; no such file exists in the lane's
   `corpus/knowledge/` (verified by directory listing and `find -name 'r4-env*'`).
8. **Reproduction not permitted.** Re-running `tools/env-diff.py` executes the
   four/six fleet gate selftests under `--fleet-root /home/vgpnk/Projects/shokunin`
   (sibling-lane mutation — out of bounds, and the counters' default mode is frozen
   for the L1). Not attempted.

## Disposition

`payload-absent` = the fabrication class. Hand-check confirms the register: the
quoted summary line is a narrative claim about an ephemeral run whose receipt,
contract, and derived inputs were never persisted in the cited repository. No fold
of the cited source contains it, and the only copy in existence is the proposal's
own prose (`lanes/tameshi/round5/SOURCES-PROPOSED.md:31`). Refuse the row.

Precedent in the same lane: round-39 refused sibling rows S137/S141 of the same
class (`corpus/lessons/round-39.md` — "quarantined `payload-absent` … no payload
is in that tree").

## Re-verification commands

```
grep -n 'S140' /home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md   # row 38
sed -n '226p' /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin && git log -S 'classified=5/6' --all   # empty
ls /tmp/r4-env-diff.json /tmp/r5-env-diff.json                                            # absent
sha256sum tools/env-diff.py                                                               # e8b47ab7cf232376…
```

## Residual risk / gaps

- A reviewer could argue the *four-gate* S140 row's real quote is
  `classified=4/4`, not the register's `5/6` span. Same outcome: `/tmp/r4-env-diff.json`
  is unpersisted and the `4/4` line is in no artifact either.
- Remote was verified reachable via `git ls-remote` (HEAD pin only); no clone or
  page fetch of github.com/VeigaPunk/tameshi-shokunin was needed since the local
  checkout is byte-identical to remote HEAD and covers all history (989 revs).
- Lane checkout and shokuknow untouched; no counters run; no tools installed.
