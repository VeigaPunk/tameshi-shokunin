# FreshnessCritic — round 13 w1 (critic, read-only)

Scope: try to break the idea that the new round-13 pin observations count as a stale-successor kill-rate re-sweep. Keep content freshness apart from mutation-verdict freshness. Put a bound on the remaining stale-successor debt. Method: read-only git (`show`, `rev-parse`, `rev-list`, `merge-base --is-ancestor`, `ls-tree`, `status --porcelain`) plus hashlib. No sibling code, gate, test or selftest was executed. No implementation was edited. Installs: none.

## Axes

- **verdict freshness**: has a mutation table been executed at the live revision?
- **content freshness**: do the pinned bytes still name the live object?
- **depth**: stays 6, no seventh case.
- **provenance**: who measured what, at which revision and time.
- **adjacency**: sibling gates stay read-only.

## Counterexamples

### CE1 — "changed", and even a same-spec rerun, is not a successor re-sweep [O]

I parsed the six embedded specs (`tools/mutate-and-run.sh:589-900` heredocs, unescape grammar `:36-49`). I counted each `@old` string in the pinned blob and in the current HEAD blob.

**Parser check:** all 65 strings give count==1 on the pinned blobs. That matches the runner's recorded assertion (`:94-97`).

| leg | count==1 at pin | count==1 at HEAD | strings that fail at HEAD |
|---|---|---|---|
| js-kimi-census | 10/10 | 9/10 | D10 count 0 |
| bash-surface-census | 10/10 | 10/10 | — (bytes unchanged) |
| bash-tsukuroi-census | 10/10 | **10/10** | — (bytes changed, 976 → 2679 L) |
| bash-mado-verify | 10/10 | **1/10** | D1, D2, D3, D6, D7, D8, D9, R1 count 2; D5 count 27 |
| bash-checklist-run | 15/15 | 15/15 | — (bytes unchanged) |
| js-claims-check | 10/10 | 10/10 | — (bytes unchanged) |

What follows:
- **mado and kimi:** the recorded spec cannot even build mutants at HEAD. The runner refuses with exit 2 before any suite run (`:47-49`, `:209`).
- **tsukuroi is the dangerous case.** The old spec still applies cleanly, so a same-spec run at HEAD would print a number that looks like a successor rate. But:
  - The suite composition has moved. The ledger's trigger T2 says the old rate's "comparability lapses" (`fleet-kill-rate-ledger.md:309`).
  - No clause map was pre-registered for the new bytes (`:312`).
  - At most, that run is the bounded "do B7/B8/B9 stay open" probe (`SKILL.md:790-792`), not the independent fresh reading (`:308`).
- **A pin read is weaker than either of these.** The ledger's own wording: "The read is hygiene and a trigger reading, not a replay guard" (`fleet-kill-rate-ledger.md:293`).

### CE2 — the standing debt set is out of date: three legs changed, not two [O]

The records name two stale legs:
- `corpus/README.md:96-97`
- `closeout-r11.md:322-326`
- `SCORECARD.md:264-267` ("4 current · 2 stale · 0 drift → 6 · 0 · 0")

At this read (2026-10-20T04:49Z) every pinned rev is an ancestor of HEAD, and HEAD blob = worktree on all six:

| leg | pin sha256 | live sha256 (HEAD = worktree) | repo HEAD | target commits since pin / last |
|---|---|---|---|---|
| kimi | 83016d45… | `5e8d591324064fff714fb85b9d254b726deb9fd9cf15261eba135ccff6db3dc0` | `1770305fae20826b39905a8251ddeca6b4957ac4` | 1 / `1a8eed5aaa32043cf109dd28ceb5cd37ccd5555e` (2026-10-19T19:41:02-03:00, +58/−32) |
| tsukuroi | 084951be… | `d17d32a35946c71c1fc195e36178aa383f4a04d7172cc579b6e9e25fa537f27e` | `9574a189a758251da5957eee8ff0f38ba2d03c7f` | 5 / `70fede2a7a890cb50a72db2d4230ee541183bf7b` (2026-10-20T00:58:24-03:00) |
| mado | d7edaab4… | `037b05dcd3f86e12e1b89ee5631f76ce95301b7c411957fad17ff0d7438a6569` | `59cfbdc3ab5e7b6aaf68f86e1b2ae8d51c938b1e` | 7 / `95cbc41fe5d5db121b89c2ddd1f953728663c5f4` (2026-10-20T01:46:14-03:00) |
| surface, checklist, claims | = pin | = pin | kagi `c2cab35b`, kumitate `1770305f` | 0 (repo commits since: 18 / 18 / 29) |

- Nothing in the ledger records the kimi move. `grep 5e8d5913` finds it only as worktree dirt in `reports/round-1-kaika-coldread.md:248-251`.
- The "live successor" shas from round 11 (`10452443…`, `93e43f8f…`) are no longer live. A successor row pinned to them would pin a revision that has already been superseded.
- **Reading now:** 3 content-unchanged · 3 changed · 0 drift.

**Debt bound [I]:** three un-swept successor measurements remain owed: tsukuroi, mado and kimi. Each needs:
- a fresh pre-registered spec cut from the live bytes, because the old spec fails or loses comparability (CE1);
- a control run;
- an appended ledger row.

None of this is closed by round 13. The kimi row is new debt and must be added as an append-only correction to the two-leg list. The historical lines must not be rewritten.

### CE3 — the observation goes stale within this wave [O]

- The wave registry was created at 04:45:35Z.
- mado committed its target at 95cbc41, 04:46:14Z.
- mado HEAD then moved again to 59cfbdc, 04:48:51Z, between two of my reads. The target blob stayed `037b05dc…`.
- tsukuroi has 13 dirty non-target paths (its round-13 work).

So any receipt is a timestamped reading. A committed `pin-dispositions.json` with no observation time, read later by `measure.py --rev`, will look current when it is not.

### CE4 — the planned freshness metric can be satisfied without measuring [I]

`SCORECARD.md:264-267` counts with `grep -c 'stale'` plus a pin read, and targets 6·0·0. Two ways to hit that target without any sweep:
- edit `PIN_*`/`REV_*` (`mutate-and-run.sh:542-553`) to HEAD;
- append a row at the live sha.

Either one is false provenance. Freshness can move only on appended rows backed by executed control + spec + table at a named revision (`fleet-kill-rate-ledger.md:310-312`).

### CE5 — "unchanged" does not make the verdict fresh [O/I]

For the three unchanged legs, the latest verdict evidence is still the replay. Round 12 records "six-leg regression PASS" (`SCORECARD.md:318`). That replay checks that the result reproduces at the pinned bytes; it is not a new reading.

The host matches the recorded toolchain:
- now: bash 5.3.15, node v24.21.0, python 3.14.7, kernel 7.2.3-arch1-3;
- recorded: ledger U1 (`fleet-kill-rate-ledger.md:218-219`);
- runner sha `75ed934d…` is unchanged.

That match is still not reuse. The case set depends on PATH and the exec mode (`incremental-pin-disposition.md:201-218`), and a current tsukuroi HEAD output line embeds `$EUID` (`tsukuroi-census.sh` @HEAD `:757-814`).

For the three changed legs, a `--regression` PASS materializes the **old** bytes (`mutate-and-run.sh:97-103`). It must never be cited as successor evidence.

## Implementation defects (sent to owners)

**`tools/pin-disposition.py` → TameshiR13.PinProbe** (file as landed at this read):
- **P0** — `re` is never imported (imports `:72-80`), but `:87-88` call `re.compile`. Every invocation, including `--selftest`, will hit a NameError at load before any JSON is emitted. Fix: `import re`.
- **P1** — `base_payload` (`:146-152`) has no `observed_at`. Without it the receipt cannot handle CE3.
- **P1** — `content_status` (`:412-424`) compares the worktree against the pin only. HEAD is never compared, so the ER-3 current/stale/drift readings cannot be derived:
  - worktree = pin but HEAD ≠ pin reads `unchanged` where ER-3 says drift;
  - HEAD = pin with a dirty worktree reads `changed`, the same as a committed successor.
  Fix: add `head_vs_pin` and `head_vs_worktree`; keep `content_status` as it is.
- **P2** — there is no ancestry field. `changed` must not be read as ER-3 `stale` without `merge-base --is-ancestor`.

**`incremental-pin-disposition.md` → TameshiR13.IncrementalKnowledge:**
- Add a §6 falsifier: re-pin or append a row without an executed sweep.
- Add `observed_at` + per-repo HEAD to the receipt invariants.
- The reuse argument itself holds.

**L1-owned `measure.py`:**
- `obj()` returns `None` silently when the file is absent (`before.json` shows `pin_dispositions: null`).
- No seat is assigned to write `pin-dispositions.json`.
- The after-measurement must assert that it is non-null.

## Smallest safe correction

- **C1 wording:** "content dispositions observed at <UTC>; verdict freshness unchanged".
- **Freshness axis row:** stays `unchanged`, as in `SCORECARD.md:319`.
- **F7:** must not move to "per-leg reuse decisions classified" (`corpus/README.md:84`). A constant `not_established` value discriminates nothing. This is a tradeoff the judge should reject if F7 is marked held.
- **Debt:** stale-successor debt goes from 2 to 3 (add kimi), recorded as append-only errata.
- **Ledger and runner pins:** byte-unchanged.

## Checks for L1 (not executed here)

1. `grep -n '^import re' tools/pin-disposition.py` must hit. Then run `python3 tools/pin-disposition.py --selftest` and expect exit 0.
2. `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin`. Predicted from this read: `.counts` = legs 6 / unchanged 3 / changed 3 / unavailable 0, with changed = kimi, tsukuroi, mado. Any `result_reuse` value other than `not_established` fails.
3. Re-run step 2 immediately before commit and diff `.legs[].head.commit` and `.legs[].worktree.sha256`. mado/tsukuroi are moving.
4. `git diff --exit-code tools/mutate-and-run.sh` (no re-pin). Then `git diff corpus/knowledge/fleet-kill-rate-ledger.md`: either empty or a purely appended block with no kill-rate.
5. `grep -nE '6 · 0 · 0|stale=0|current=6|re-sweep(s)? (landed|ran)|successor row' LOG.md SCORECARD.md corpus/README.md` on the round-13 diff → no freshness claim.
6. `git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin rev-list 175de6ba..HEAD -- scripts/kimi-census.mjs` → `1a8eed5…`. Record it as the third debt row.
7. `python3 .ufo/evidence/round-13/measure.py --rev <after>` → `pin_dispositions` non-null and six rows.
8. Optional reproduction of CE1: count each embedded `@old` in `git show HEAD:<path>`. Expected count==1: kimi 9/10, tsukuroi 10/10, mado 1/10.

## Addendum — PinProbe reply (re-read, not executed)

- **P0 withdrawn as a landed defect.** `import re` is now present at
  `tools/pin-disposition.py:86`, and `import datetime` at `:82`. My earlier
  read of `:72-80` caught the file mid-edit, so P0 was a transient. It is not
  a defect in the landed bytes. L1 check 1 still applies.
- **P1 `observed_at`: resolved, with one nuance.** `:567-569` stamps it
  *after* all six legs have been read (`:562`). It is therefore the end
  bound of the read window, not the start. That is fine as long as receipts
  and docs call it the end instant, not "the moment each row was read".
- **P1/P2 (`head_vs_pin`, `head_vs_worktree`, ancestry): declined** by
  PinProbe as a minimality call under L1. I accept this as a tradeoff, not a
  defect, on these conditions:
  - **Drift from the receipt alone:** a reader can derive the ER-3 readings
    from the separate `pinned.commit` / `head.commit` / `head.blob_sha256` /
    `worktree.sha256` fields.
  - **Stale needs an outside check:** "stale" cannot be read from the receipt
    alone, because it requires ancestry. L1 records must not call a `changed`
    row "stale" unless they cite a separate
    `git merge-base --is-ancestor <pinned> <HEAD>` read. At my read, all six
    pinned revs were ancestors.
  - **Committed versus uncommitted:** `content_status: changed` alone never
    separates a committed successor from a dirty worktree. Compare
    `head.blob_sha256` with `worktree.sha256`.
