# RGSpecD — C1 defect drafting, class D (reported-but-unasserted surfaces)

Seat: `TameshiR16.RGSpecD` · wave round-16/w1 · lane root `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
Class: **§13.5 — reported-but-unasserted surfaces** (FAIL-CLOSED detail tails / stderr diagnostic / `durationMs` / JSON `citations` fields).

## 1. Materialization + pin

```
$ git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show \
    364f1d5954158ef8844bca4a5fef57b05d2f2ca5:scripts/round-gate.mjs > /tmp/tameshi-r16-RGSpecD/round-gate.mjs
$ sha256sum /tmp/tameshi-r16-RGSpecD/round-gate.mjs
f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9   # MATCHES the claimed pin
$ wc -l → 1511   # matches matrix §13.10 #1
```

Sibling repo untouched (read via `git show` only). Scratch: `/tmp/tameshi-r16-RGSpecD/`.

## 2. Pristine control pulse (allowed once; no mutant was run)

```
$ node /tmp/tameshi-r16-RGSpecD/round-gate.mjs --selftest
ROUND_GATE_SELFTEST: 60/60 pass
VERDICT: PASS        exit=0
```

No mutant was built or executed — predictions below are **pre-registered** before any sweep.

## 3. Class-D surface read (grounding, all line refs into the pinned blob)

- `failClosed()` `:596-619`: stderr diagnostic `:615` (`round-gate: fail-closed — ${token}: ${detail}`); text verdict `:617`; fail-closed JSON body `:597-614` incl. `durationMs` `:613` and zeroed `citations` `:609-612`.
- Checks asserting fail-closed behavior read **stdout token + exit code only**: fcA `:1188`, fcB `:1193`, fcC `:1198`, fcD `:1206`, fcE `:1212` (adds `/no upstream|exit 128/` against *stdout*), fcF `:1218`, rt3 `:1435-1436`, rt5 `:1450`, jFc `:1282-1284`.
- `grep -n stderr`: suite stderr reads exist only on the **exit-64** paths (u1–u5 `:1224-1245`, rt4 `:1441-1442`) — no check reads a fail-closed run's stderr.
- `durationMs` assertions: exactly one — `typeof j.durationMs === 'number'` at `:1263`, inside **jClean**, which parses `jClean.stdout` (audit body written `:671`, emitted `:673-674`). jFc `:1279-1286` reads contract/verdict/findings/errors only. rt7 `:1470-1473` never reads `durationMs`.
- `citations` JSON reads: `j.citations.checked === 0` `:1264` (jClean only); `citations.external` `:1122`, `:1350`, `:1357`; `originProbeable`/`unverifiable` `:1374-1375`. **`mainProbeable`, `unresolved`, `notAncestor` are read by no check** (text-side findings carry them via `citedDetail` `:389-394`, which r22 `:1081` / r23 `:1101` pin at substring level).
- `citations.mainProbeable` assignment `:387` copies the lazily probed local (`:333`, `:335`); probes use the local via `mainProbeableNow()` (`:366`, `:381`), so mutating the copy does not move any finding.

## 4. Candidates (spec fragment: `.ufo/waves/round-16/w1/RGSpecD.spec`)

All `@old` counts verified post-unescape against the pinned blob with a byte-exact counter: **each = 1** (command in §5). The spec file's escaped `@old`s reproduce the same three strings; the multi-line RGD2 anchor uses a real `\n` escape to span `:613-615` (parser `unescape()` at tools/mutate-and-run.sh `:267-283` allows `\n`).

### RGD1 — fail-closed stderr diagnostic drops the detail tail

- `@old` `process.stderr.write(`round-gate: fail-closed — ${token}: ${detail}\n`);` — **count = 1** (`:615`)
- `@new` `process.stderr.write(`round-gate: fail-closed — ${token}\n`);`
- Arm class: §13.5 #1 — the stderr diagnostic is reported but read by nothing.
- **Prediction: SURVIVED.** fcA `:1188` / rt3 `:1435` / rt5 `:1450` match `/ROUND_GATE: FAIL-CLOSED \(<TOKEN>\)/` against `String(<r>.stdout)`; fcB `:1193`, fcC `:1198`, fcD `:1206`, fcF `:1218` match `/<TOKEN>/` on stdout; fcE `:1212` probes stdout text that is the *detail* string (contains `exit ${ahead.status}` + stderr first line, `:460`) — none touch `r.stderr`. jFc `:1282-1284` asserts `j.errors === 1` (`:607`, unchanged) and never reads `findings[0].detail` or stderr. Exit stays 2 (`:618`).

### RGD2 — fail-closed JSON body reports a constant `durationMs`

- `@old` `    durationMs: Math.max(0, Date.now() - started),\n  };\n  process.stderr.write` — **count = 1** (`:613-615`; the trailing `process.stderr.write` disambiguates this `durationMs` from the audit `:671` and tracked `:569` copies, which are followed by `if (opts.json)`)
- `@new` `    durationMs: 0,\n  };\n  process.stderr.write`
- Arm class: §13.5 #3 — `durationMs` type-pinned once, value unread; here the fail-closed copy is read by *no* assert at all.
- **Prediction: SURVIVED.** jFc `:1282-1284` reads only `contract`, `verdict`, `findings[0].kind`, `errors` — `durationMs` unexamined; key-set equality runs only in jClean `:1254-1261` on the audit body (mutant keeps the key, still a `number`, so even a hypothetical key set/type check stays green). Text-mode fc checks never see the JSON body (`:616` gate).

### RGD3 — `citations.mainProbeable` reported as `null` on probeable runs

- `@old` `    citations.mainProbeable = mainProbeable;` — **count = 1** (`:387`)
- `@new` `    citations.mainProbeable = null;`
- Arm class: §13.5 #4 — JSON `citations.mainProbeable` is computed but read by no check.
- **Prediction: SURVIVED.** The copy at `:387` is report-only: probes branch on the `mainProbeable` local via `mainProbeableNow()` (`:335`, `:366`, `:381`), so findings, `external`/`unresolved`/`unverifiable` buckets, and `originProbeable` are unchanged. Fixtures with citations populated — r22 `:1077` (`deadbeef1234`, main probeable → `unresolved`), r23 `:1096` (side sha → `notAncestor`), r24 `:1117/1120` (origin sha → `external`), rn/rl `:1347/:1354`, rnone `:1368` — assert only `external`/`unverifiable`/`originProbeable`/findings; rnone's `mainProbeable` field would flip `true→null` yet `:1374-1376` never reads it. jClean's `fxBigReport` carries no backticked tokens (`:785-787`) so `:1264` only checks `citations.checked === 0`.

## 5. Evidence — commands actually run

| # | Command | Exit | Key output |
|---|---|---|---|
| 1 | `git -C …/kumitate-shokunin show 364f1d59…:scripts/round-gate.mjs > /tmp/…` | 0 | blob materialized |
| 2 | `sha256sum` + `wc -l` on materialized blob | 0 | `f890e277…a834d3e9`, 1511 lines |
| 3 | `python3` literal counter over 6 candidate `@old` strings | 0 | D1_stderr=1, D2_durms=1, D3_mainprobe=1 (also alt_checked=1, alt_notancestor_push=1, alt_selftest_count=1 — alternates evaluated and dropped) |
| 4 | `grep -n stderr` on pinned blob | 0 | suite stderr asserts confined to `:1224-1245`, `:1441-1442` (exit-64 paths) |
| 5 | `python3` unescape-mirroring counter on the shipped spec's `@old`s | 0 | RGD1=1, RGD2=1, RGD3=1 |
| 6 | `node /tmp/…/round-gate.mjs --selftest` (pristine only) | 0 | `ROUND_GATE_SELFTEST: 60/60 pass`, `VERDICT: PASS` |

Attempted: `source tools/mutate-and-run.sh list <spec>` → exit 64 (`unknown argument: list`; the script's arg loop runs on source — no harm, spec was validated by mirroring its own `unescape()`/count logic instead).

## 6. Predictions summary (pre-registered)

| Defect | Prediction | Suite observation expected |
|---|---|---|
| RGD1 | SURVIVED | all 60 checks green; stderr untested on fail-closed paths |
| RGD2 | SURVIVED | jFc green; `durationMs` value/type unread on the fail-closed body |
| RGD3 | SURVIVED | r22/r24/rnone green; `j.citations.mainProbeable` asserted nowhere |

Diversity note for L1: all three predict SURVIVED by construction — class D *is* the unasserted-remainder class (analogous to the pair's D2/B10 survivors). If L1 needs kill-mix in the 10-mutant sweep, RGD3 could be swapped for a variant that corrupts `citations.checked` in the fail-closed body (`checked: 0` → `checked: 1` at `:610`, count=1) — but note even that is predicted SURVIVED (jFc never reads `j.citations`), so class D honestly yields no predicted kills; the sweep's kill-rate should come from other classes.

## 7. Tooling

No installs or upgrades performed (existing `git`, `node`, `python3`, `bash` sufficed). Pacman untouched per the host-wide pause.

## 8. Risks / blockers

- None blocking. Residual: predictions rest on a static read of the 60 checks at this pin (all cites verified against the blob); §13 labels the whole projection "static" for the same reason — the sweep resolves it.
- If L1 prefers `@old`s confined to a single line, RGD2's anchor can be shortened to `durationMs: Math.max(0, Date.now() - started),\n  };\n  process.stderr.write` (still count=1) — already written that way.
