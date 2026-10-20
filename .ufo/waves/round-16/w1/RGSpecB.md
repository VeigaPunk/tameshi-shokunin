# RGSpecB — class B defect drafting (fail-closed arms/tokens)

Seat: TameshiR16.RGSpecB · wave round-16/w1 · lane tameshi-shokunin.
Spec fragment written: `.ufo/waves/round-16/w1/RGSpecB.spec` (3 candidates, spec v1).
No mutant was executed. Pre-registration preceded any sweep; only the pristine
selftest was run (allowed by the Target).

## 1. Pin verification

```text
$ git -C kumitate-shokunin show 364f1d5954158ef8844bca4a5fef57b05d2f2ca5:scripts/round-gate.mjs > /tmp/tameshi-r16-RGSpecB-a/round-gate.mjs
$ sha256sum → f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9   (MATCHES declared pin)
$ wc -l → 1511
```

Sibling repo untouched (materialized via `git show` only; no checkout/write).

## 2. Baseline control (pristine, run once — allowed)

```text
$ cd /tmp/tameshi-r16-RGSpecB-a && node round-gate.mjs --selftest
exit 0 — ROUND_GATE_SELFTEST: 60/60 pass — VERDICT: PASS — node v24.21.0, 3.69 s
```

Relevant observed lines (numbered checks):
- `[32]` fcA: `exit=2 ROUND_GATE: FAIL-CLOSED (REPORTS_DIR_MISSING) --reports-dir …/no-such-reports is absent`
- `[36]` fcE: `exit=2 … (UPSTREAM_MISSING) --repo …: exit 128 fatal: no upstream configured for branch 'main'`
- `[37]` fcF: `exit=2 … (MAIN_REPO_NOT_GIT) …`
- `[45]` jFc: `exit=2 verdict=FAIL-CLOSED kind=REPORTS_DIR_MISSING`
- `[54]` rt3: `exit=2 … (NO_FILED_REPORTS) filed=1 …`
- `[56]` rt5: `exit=2 … (MAIN_REPO_NOT_GIT) --main-repo …/not-a-repo is not a git work tree`

## 3. Candidates (class B — fail-closed arms/tokens, §13.3/§13.6)

### RGD-B1 — KILLED (predicted)

| field | value |
|---|---|
| description | Main-path `REPORTS_DIR_MISSING` call site (`:647`) emits the wrong declared token (`MAIN_REPO_NOT_GIT`). Same-arm, wrong-token defect. |
| @old | `return failClosed(opts, mode, 'REPORTS_DIR_MISSING',` — literal count in pinned blob: **1** |
| @new | `return failClosed(opts, mode, 'MAIN_REPO_NOT_GIT',` |
| arm class | fail-closed token, covered species (main/audit site, `:646-648`) |
| prediction | **KILLED** — fcA runs `--reports-dir …/no-such-reports` in audit mode (`:1186`) and asserts `/ROUND_GATE: FAIL-CLOSED \(REPORTS_DIR_MISSING\)/` (`:1188`); jFc runs the same arm with `--json` (`:1278`) and asserts `findings[0].kind === 'REPORTS_DIR_MISSING'` (`:1283`). Both emit `MAIN_REPO_NOT_GIT` under the mutant → two checks FAIL → suite exit 1. |

### RGD-B2 — SURVIVED (predicted)

| field | value |
|---|---|
| description | The *identical* one-token defect cut at the **tracked-mode** `REPORTS_DIR_MISSING` site (`:527`) — the uncovered call-site species (§13.3, §13.6 #2). |
| @old | `return failClosed(opts, 'tracked', 'REPORTS_DIR_MISSING',` — literal count in pinned blob: **1** |
| @new | `return failClosed(opts, 'tracked', 'MAIN_REPO_NOT_GIT',` |
| arm class | fail-closed token, uncovered call-site species |
| prediction | **SURVIVED** — the token is pinned (fcA/jFc), but only via the `:647` species. Every `--tracked` fixture passes an existing `--reports-dir`: rt1/rt2/rt6/rt7/rt8 use `trackedArgs` over `fxTrackedMain`-built dirs (`:1407`-`:1483`), rt3's dir exists with one filed report (`:1432`), rt5's `tkClean.reports` exists so the `:526` arm is skipped and `:530`'s own token still satisfies `/FAIL-CLOSED \(MAIN_REPO_NOT_GIT\)/` (`:1450`). No run reaches `:527`, so no check observes the wrong token. Deliberate twin of RGD-B1: same edit text species, different call-site species — the §13.3 asymmetry as a mutant pair. |

### RGD-B3 — SURVIVED (predicted)

| field | value |
|---|---|
| description | Catch-all `INTERNAL_ERROR` token (`:683`) renamed to another declared token (`UPSTREAM_MISSING`). |
| @old | `return failClosed(opts, mode, 'INTERNAL_ERROR', e && e.message ? e.message : String(e), [], started);` — literal count in pinned blob: **1** |
| @new | `return failClosed(opts, mode, 'UPSTREAM_MISSING', e && e.message ? e.message : String(e), [], started);` |
| arm class | INTERNAL_ERROR net — the only declared token with zero fixture coverage (§13.3 "none", §13.6 #1, PU3) |
| prediction | **SURVIVED** — two independent reasons. (a) Reachability: no fixture throws inside `main`'s `try` (`:641-684`); a throw would itself be a bug — the baseline shows every run exits 0/1/2/64 through declared paths. (b) Detection: even if a fixture did throw, the fail-closed verdict line cannot be parsed by `parseFindings` (`:857-860`), the only `observed` feeder; the meta-check (`:1487-1493`) iterates `FINDING_KINDS` (`:171-176`), which excludes all seven fail-closed tokens — the meta-check is *structurally blind* to this family (§13.3). A renamed token would at most appear in the `(TOKEN)` slot of a line no check regexes for `INTERNAL_ERROR` specifically. |

## 4. Rejected alternates (for the L1 pool, not in spec)

- `UPSTREAM_MISSING` at the **main-repo** site (`:483-489`, `token: 'UPSTREAM_MISSING',` — the second of 2 occurrences): predicted SURVIVED, second uncovered species (§13.6 #3). Rejected here only to keep the slate at 3 and because RGD-B2/B3 already cover the species/net probes; a strong reserve candidate if L1 wants a wider net. `@old "            token: 'UPSTREAM_MISSING',"` count==1 with the 12-space indent (verified: bare `token: 'UPSTREAM_MISSING',` is count 2, the indented line is unique).
- `return 2` → `return 0` inside `failClosed` (`:618`): predicted KILLED but nearly global (every fail-closed fixture flips) — low diagnostic value, better suited to another class or a coarse-net probe.
- `FAIL-CLOSED` line-shape edits (`:604`, `:617`): predicted KILLED via fcA's parenthesized-token regex; class-A-adjacent (output shape), left for that seat.

## 5. Prediction summary

| defect | site | species | predicted | would be observed by |
|---|---|---|---|---|
| RGD-B1 | `:647` | covered | KILLED | fcA `[32]`, jFc `[45]` |
| RGD-B2 | `:527` | uncovered | SURVIVED | nothing (no fixture reaches the arm) |
| RGD-B3 | `:683` | uncovered + structurally blind | SURVIVED | nothing (no throw; meta-check blind) |

Projected contribution to the 10-defect leg: 1 kill + 2 survivors from this class —
consistent with §13.3/§13.6: the suite's fail-closed coverage is hand-regex
token assertions that cannot see call-site species or the catch-all net.

## 6. Evidence & provenance

- Reads: `/tmp/tameshi-r16-RGSpecB-a/round-gate.mjs` (pinned blob, ranges
  `:99-203`, `:439-563`, `:599-703`, `:704-903`, `:1176-1303`, `:1390-1511`);
  `tameshi-shokunin/corpus/knowledge/arm-class-matrix.md:298-503` (§13);
  `tameshi-shokunin/tools/mutate-and-run.sh` (spec v1 grammar, ledger intent).
- Uniqueness: `python3` literal `blob.count(@old)` → 1 for each of the three
  @old strings (shown inline per candidate). `@new != @old` for all.
- Commands run: `git show` (materialize), `sha256sum`/`wc`, `node --selftest`
  (pristine only), `mkdir`/`ls` on the wave dir. No mutant built, no suite run
  against a mutant, no lane-repo file written other than the two assigned
  artifacts under `.ufo/waves/round-16/w1/`.
- Scratch: `/tmp/tameshi-r16-RGSpecB-a/` (pinned blob copy; no lane writes).
- Tools installed: none (existing git/node/python3/bash sufficed; pacman paused
  per contract and nothing was needed).

## 7. Risks / recommendations

1. RGD-B2's survival depends on "no fixture passes a missing --reports-dir to
   --tracked" — verified by reading all rt* call sites (`:1407`-`:1483`); if a
   sibling seat's fixture additions change that, the verdict flips [INFERENCE
   boundary: fixture set is read as of the pinned sha].
2. RGD-B3 is the cleanest "structurally blind" demonstrator in the leg; if the
   ledger wants at most one survivor per family, prefer keeping B3 over B2
   (B2 is also redundant *as a kill* — its twin B1 already proves the token).
3. Recommend L1 pair B1/B2 in the ledger write-up as one recorded observation
   (same-token species asymmetry) even though they are two spec entries.
