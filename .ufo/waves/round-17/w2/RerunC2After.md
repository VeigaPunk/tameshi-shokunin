# RerunC2After — independent re-run of the C2 after measurement at `eb7838b`

Seat `TameshiR17.RerunC2After-2` (leaf, no delegation). Graded commit:
`eb7838b16490ca7ba17ea3242ade76a61f744af2` (`rev_resolved` equal, detached). All
runs were in a fleet-mirror clone:

```
W=$(mktemp -d /tmp/tameshi-r17w2-RerunC2After-XXXXXX); mkdir $W/fleet
for s in /home/vgpnk/Projects/shokunin/*-shokunin; do
  [ "$s" = /home/vgpnk/Projects/shokunin/tameshi-shokunin ] || ln -s "$s" $W/fleet/; done
git clone -q /home/vgpnk/Projects/shokunin/tameshi-shokunin $W/fleet/tameshi-shokunin
git -C $W/fleet/tameshi-shokunin checkout -q --detach eb7838b16490ca7ba17ea3242ade76a61f744af2
```

Clone HEAD after all runs: `eb7838b16490ca7ba17ea3242ade76a61f744af2`; `git status
--porcelain` empty (no row wrote into the graded clone). No tool installs or
upgrades were needed.

## C2 after — commands, exits, key lines

1. Baseline-tagged registry, JSON:
   `python3 tools/registry-check.py --rev eb7838b16490ca7ba17ea3242ade76a61f744af2 --tag baseline --json`
   **exit 0**; human trailer on stderr `REGISTRY_CHECK: held=23/23 superseded=1`;
   JSON `{schema: tameshi-registry-check-report-v1, rev_resolved:
   eb7838b16490ca7ba17ea3242ade76a61f744af2, registry_sha256:
   98bdc23ce4880fc3d23d169c38e36c2a9f2c69c273b936e868a7ddfd459e0630, held: 23,
   total: 23, superseded: 1, exit: 0, tags: ["baseline"]}`, 24 row entries
   (23 active + 1 superseded).
2. Full registry, no `--tag`:
   `python3 tools/registry-check.py --rev eb7838b16490ca7ba17ea3242ade76a61f744af2 --json`
   **exit 0**; `REGISTRY_CHECK: held=28/28 superseded=1`; same
   `rev_resolved`/`registry_sha256`, `held: 28, total: 28, superseded: 1, exit:
   0`, 29 row entries. The 5 rows beyond the baseline set are
   `evidence-disposition-round17-before`, `registry-check-selftest`,
   `measure-round17-selftest`, `trace-inputs-round17-selftest`,
   `assemble-round17-selftest`; all held.
3. Monitor selftest: `python3 tools/registry-check.py --selftest` **exit 0**,
   `SELFTEST: PASS (34 cases)`, including `gitdir-scrub-rev`,
   `gitdir-scrub-row`, `rev-non-hermetic-argv`, `rev-external-declared`,
   `superseded-runs-excluded`, `tag-selects-any`, `json-report`.

`registry_sha256` equals the clone's `tools/registry.json`
(`sha256sum` = `98bdc23ce4880fc3d23d169c38e36c2a9f2c69c273b936e868a7ddfd459e0630`),
which also equals the live lane's copy at the time of the run — so grading the
clone's own registry is grading the round-17 registry from the claim.

Cross-check base vs full: shared rows have identical `expect/got/held/status`;
the tag filter changes only the row set, not outcomes.

## Differing rows (all of them) and cause

No active row differs in either run (`differing active: []`). The one
non-held row is the deliberately superseded one, present in both runs:

```
ROW evidence-disposition-round14-superseded superseded expect=0 got=2
```

- Registry entry: `tools/registry.json:249-271` — `status: superseded`
  (`:266`), `superseded_by: evidence-disposition-round17` (`:267`, an existing
  active row that holds). It is excluded from N/M by construction (`tools/registry-check.py:544-554`);
  the human line is printed without `held|differs` (`:562-568`); exit code
  considers active rows only (`:554`).
- Cause of `got=2`: the old command is
  `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json`
  and it exits 2 `could_not_evaluate` / `expected_input_digest_mismatch`:
  `tools/mutate-and-run.sh: observed fb6d86d59b5c9285864c9ebfa19d5a6f8938e91c47877a6d25b451a1da03001a expects 75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5`.
  The pin is `.ufo/evidence/round-13/expected.json:12`
  (`inputs["tools/mutate-and-run.sh"]`); `75ed934d…` is the pinned round-13-era
  file bytes (identical to `git show 606716f:tools/mutate-and-run.sh`, the
  file's last version before the round-16 edits). The runner changed at
  round 16 (`c699c8c`: `89722ddb…`, `05a2247`: `0673d2e5…`) and at landing
  (`2a22ade`/`eb7838b`: `fb6d86d5…`, the jj repo-identity/GIT_* fixes). Manual
  re-execution of the row's exact argv reproduced exit 2 and the identical
  message.
- This is the documented historical outcome, not a surprise: `SKILL.md:1601`
  marks the round-14 recipe historical with the round-17 live entry, and
  `SKILL.md@98bea7d:1681` already stated `--root .` "returns 2
  `expected_input_digest_mismatch` by design" since round 16.
- The same row also reports `got=2` at the pre-landing rev (observed
  `0673d2e5…`), so it was already red before `eb7838b`; marking it superseded
  uncovers a known drift, it does not hide a new regression.

## Before leg (spot check only; the dedicated before seat owns the full run)

- `python3 tools/registry-check.py --rev 98bea7da5801f4bc58e4187690ee1687c8a5061f --registry <clone>/tools/registry.json --only evidence-disposition-round17 --json`
  → exit 1; row `got=2` differs, `dispositions_missing`
  (`.ufo/evidence/round-17/dispositions.json` absent at that rev). The
  disposition capability indeed differs at `98bea7d`.
- `... --only evidence-disposition-round14-superseded --rev 98bea7d ...` → exit
  0, `held=0/0 superseded=1`; that row `got=2` (same digest mismatch, observed
  `0673d2e5…`).
- Stored `.ufo/evidence/round-17/c2-before-98bea7da5801f4bc58e4187690ee1687c8a5061f.json`
  reports `held: 22, total: 23, superseded: 1, exit: 1` with exactly that row
  differing — agreement.

## After receipts — agreement and the one fixed difference

- Stored `.ufo/evidence/round-17/c2-after-2a22ade.json` (`rev` =
  `2a22adeb7d1de5e7189e62ce41ac679d71a97b44`) reports `held: 22/23, exit: 1`.
  Its only differing active row is `evidence-disposition-selftest` `got=1`
  (`.ufo/evidence/round-17/c2-after-2a22ade.txt:12`). Diffing it against this
  rerun: **the only difference is that row**, now `got=0 held`.
- Cause of the fix: `eb7838b` routes selftest fixture git calls through
  `_selftest_git_env()` (`tools/evidence-disposition.py:1900-1913`), which
  scrubs `GIT_*` and sets `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`
  and author/committer identity; `_git`/`_git_raw` use it (`:1915-1931`), so the
  scrubbed-environment `commit-tree` has an identity again.
- The live lane at `eb7838b` has untracked
  `.ufo/evidence/round-17/c2-after-eb7838b.json/.txt` (read-only inspection).
  That receipt matches this rerun field-for-field (`held: 23/23, exit: 0`, same
  `registry_sha256`, 24 rows, only the superseded row non-held), so the
  post-fix after measurement is independently reproduced.
- Full-registry receipt `.ufo/evidence/round-17/registry-full-2a22ade.json` is
  `held: 27/28, exit: 1`; this rerun at `eb7838b` is `28/28, exit: 0`. The
  difference is exactly the fixed `evidence-disposition-selftest` row.

## Residual risk / notes (non-blocking)

- `pin-disposition-read` (`tools/registry.json:105-131`, `external: true` at
  `:130`) is a baseline row whose argv contains the absolute live-fleet path
  `/home/vgpnk/Projects/shokunin`. Baseline `held=23/23` is therefore partly
  fleet-state-dependent by declaration (it reports `"unavailable": 0`). When
  `registry-check.py` runs from a clone, `fleet_root` is derived from the source
  lane's parent (`tools/registry-check.py:1267`), i.e. the temporary mirror, so
  this token is not annotated `non_hermetic_argv`; run from the live lane it
  would be annotated (allowed by `external: true`). No claim impact, but the
  reproduction is not fully rev-hermetic for that one row.
- The committed after receipt in-tree is pre-fix (`2a22ade`, 22/23); the green
  `eb7838b` receipt is untracked in the live lane. The L1 may want to commit it
  so the landing SHA carries its own after evidence.
- No LSP server/tool was available in this environment; caller/definition/
  diagnostic checks were done by direct execution of every row plus the
  monitor's 34-case selftest, which exercises the same code paths (superseded
  exclusion, tag selection, non-hermetic detection, exit codes).

## Verdict

**C2 after holds**: at `eb7838b` the baseline set is `held=23/23 superseded=1`
(exit 0) and the full registry `held=28/28 superseded=1` (exit 0); the only
non-held row is the declared superseded round-14 command (pinned
`tools/mutate-and-run.sh` digest mismatch), and no active row differs.
