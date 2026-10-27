# T51LabSandboxLeak — round-51 C2 sandbox-id leak confirmation (falsifier report)

- Seat: `T51LabSandboxLeak` (leaf; no subagents)
- Round: 51 (hyaku run 9, L1 TameshiR51) · wave w1
- Item: independently test the L1 claim that K_GONE_ARM, K_AMBIG_GT, K_SHAPE_OPTIN
  survive the sweep **only** because the sandbox directory name embeds the defect id
  (whose substring satisfies the gate's unanchored verdict-word grep over output that
  prints scratch paths)
- Date: 2026-10-26

## 1. Build — mutants byte-identical to the sweep

Target: kagi `corpus/drift-pins.sh` @ `e64e81b8eb96f3682b00c1e7a291e84420b280fa`.
Command that shows the pin:

```
git -C /home/vgpnk/Projects/shokunin/kagi-shokunin show e64e81b8eb96f3682b00c1e7a291e84420b280fa:corpus/drift-pins.sh
sha256sum = c138d34c7f0dfe950fce0e5e6672cc788b5ad080bc388d4aef118db0e6c70feb (matches spec header; 451 lines; mode 100755)
```

All ten mutants rebuilt from `.ufo/evidence/round-51/c2/bash-drift-pins.defects.spec`
(one `@old` per defect, asserted to occur exactly once in the pinned bytes).
Every mutant sha256 equals the sweep's recorded mutant sha in
`.ufo/evidence/round-51/c2/sweep/results.tsv`:
`mutants-sha.csv` (10/10 `True`). The mutant set is therefore identical to the one
the sweep ran; any verdict difference is attributable to the suite environment, not
to different bytes.

## 2. Suite form (reproduced from the sweep)

The spec header records the suite as "hermetic `env -i … bash "$MUTANT" --selftest`".
The guarded form is `tools/mutate-and-run.sh`'s sandbox template
(`grep -n 'sandbox-\$DEFECT_ID' tools/mutate-and-run.sh` → lines 1418–1428):

```
h="$WORKDIR/sandbox-$DEFECT_ID"; mkdir -p "$h/home" "$h/tmp" && cd "$h" &&
exec env -i PATH="$PATH" HOME="$h/home" TMPDIR="$h/tmp" LC_ALL=C
  GIT_CONFIG_NOSYSTEM=1 GIT_CEILING_DIRECTORIES="$h" bash "$MUTANT" --selftest
```

Reproduced verbatim (driver `work/run_suite.sh` in scratch — not a deliverable).
Three sandbox-name forms, 3 repeats each (all repeats identical):

- **A** — `sandbox-<DEFECT_ID>` (exactly the sweep form; A control = green, mirroring
  sweep `CONTROL: GREEN`)
- **B** — `sandbox-n<ordinal>` (one variable changed: neutral name, no defect-id token)
- **C** — verdict-word sandbox names on purpose: `MOVED-COUNT-LINK` for the KILLED
  mutants (K_MODE_CMP, K_COUNT_GE), `GONE-AMBIG-SHAPE` for K_GONE_ARM

## 3. Results (A vs B vs C; per-run raw outputs in `T51LabSandboxLeak/raw/`, table in `T51LabSandboxLeak/README.md`)

| defect | A (id-named) | B (neutral) | C (verdict-word name) |
|---|---|---|---|
| K_MODE_CMP | KILLED exit 1 (`FAIL mode drift: exit 0 want 1`) | KILLED exit 1 (same) | KILLED exit 1 (same) |
| K_GONE_ARM | **SURVIVED exit 0 PASS 13/13** | **KILLED exit 1 FAIL `symbol gone: no /GONE/ in output`** | SURVIVED exit 0 PASS 13/13 |
| K_AMBIG_GT | SURVIVED exit 0 PASS 13/13 | KILLED exit 1 FAIL `symbol ambiguous: no /AMBIG/ in output` | — |
| K_COUNT_GE | KILLED exit 1 (`FAIL count drift: no /COUNT.*#1->#2/`) | KILLED exit 1 (same) | KILLED exit 1 (same) |
| K_SHAPE_OPTIN | SURVIVED exit 0 PASS 13/13 | KILLED exit 1 FAIL `shape drift: no /SHAPE/ in output` | — |
| S_SHA_CMP, S_HARDLINK, S_POLICY, S_DUP_UNIQ, S_USAGE_EXIT | SURVIVED exit 0 | SURVIVED exit 0 (all) | — |
| CONTROL (pristine) | exit 0 PASS 13/13 | exit 0 PASS 13/13 | — |

Only the three kill-aimed misses flip with the sandbox name; no other verdict flips.
**The hypothesis was not falsified — it is confirmed.**

## 4. Mechanism (why the name matters)

The gate's selftest `run()` helper checks each case as (gate `corpus/drift-pins.sh`,
line numbers on the pinned blob; shown by `grep -n 'grep -q' <pinned>`):

- L399: `out=$("$0" --baseline "$base" --symbols "$sym" 2>&1) && rc=0 || rc=$?`
  → captures the child's full stdout+stderr, *including scratch paths*.
- L403: `elif ! grep -q "$3" <<< "$out"; then` → an **unanchored** substring grep for
  the expected verdict word over that captured output.
- L158: `printf 'DRIFT   %s %s\n' "$p" "${diffs[*]}"` → when a pinned file drifts
  (e.g. b.txt's content changes in the "symbol gone"/"symbol ambiguous" cases, env.txt
  in "shape drift"), the emitted DRIFT line prints the absolute path `$p`, which is
  under `$TMPDIR` = `…/sandbox-<DEFECT_ID>/tmp/tmp.XXX/…`.

For K_GONE_ARM the mutated site is L231 (`if [[ "$n" -eq 0 ]]` → `-eq -1`); the
"symbol gone" case (L423) then prints no `GONE` line, but the run's captured output
still contains the DRIFT line `DRIFT …/sandbox-K_GONE_ARM/tmp/…/b.txt sha …`
(shown by instrumented run: `CASE symbol gone rc=1` + DRIFT line). `grep -q GONE`
matches the `K_GONE_ARM` token inside that path → case passes. With the neutral
sandbox `sandbox-n2` the same DRIFT line lacks the token → `grep -q GONE` fails →
`FAIL symbol gone: no /GONE/ in output` (raw `K_GONE_ARM-B-r1.out`). Identical story:
K_AMBIG_GT site L234 (`-gt 1` → `-gt 2`), case L426, token `AMBIG`; K_SHAPE_OPTIN
site L220 (`"shape"` → `"shaped"`), case L436, token `SHAPE`.

The two KILLED mutants are *not* maskable this way: K_MODE_CMP's failing case is an
exit mismatch (`exit 0 want 1`; check at L402 fires on `$rc` before the grep), and
K_COUNT_GE's pattern is `/COUNT.*#1->#2/` — the path token `COUNT` alone cannot supply
`#1->#2`. C-form runs confirm both stay KILLED under `MOVED-COUNT-LINK`, while
K_GONE_ARM is resurrected under `GONE-AMBIG-SHAPE` (raw `K_GONE_ARM-C-r1.out`).

## 5. Verdict

- Falsification attempt: **failed to falsify**. A single-variable change (sandbox name)
  flips exactly the three claimed survivors to KILLED; no other verdict flips; the
  mechanism (path-embedded defect id satisfying an unanchored `grep -q` at L403) is
  directly observed.
- Under neutral sandboxes the sweep's measured kill rate would be 5/10
  (2/10 → 5/10): K_GONE_ARM, K_AMBIG_GT, K_SHAPE_OPTIN are *detectable* defects whose
  death was masked by the suite's own id-named sandbox — i.e. the three prediction
  misses are suite artifacts, not equivalent mutants.
- Minimal red/green pair kept in the deliverable: `red-gone-id.sh`
  (sandbox-K_GONE_ARM → PASS 13/13, exit 0) vs `green-gone-neutral.sh`
  (sandbox-n2 → FAIL 1/13, exit 1), with outputs and exit codes.

## Tooling

No tools installed or updated (records: none). No counters run; the gate's own
`--selftest` was run only inside the reproduced sweep-form suite on scratch copies.

## Summary

1. Ten mutants rebuilt from the frozen spec are byte-identical to the sweep's (sha match 10/10).
2. Suite form reproduced exactly (guarded `env -i` sandbox from mutate-and-run.sh lines 1418–1428).
3. A (sandbox-<DEFECT_ID>) reproduces sweep verdicts: 2 KILLED / 8 SURVIVED, control green.
4. B (neutral sandbox-nN) kills all three misses: K_GONE_ARM, K_AMBIG_GT, K_SHAPE_OPTIN exit 1 with `no /WORD/ in output`.
5. No other verdict flips; 3/3 repeats identical.
6. Mechanism confirmed: L403 unanchored `grep -q "$3"` over captured output (L399) matching the defect-id token inside scratch paths printed by DRIFT lines (L158).
7. C: `GONE-AMBIG-SHAPE` resurrects K_GONE_ARM; `MOVED-COUNT-LINK` does not mask the two kills (exit-mismatch / `#1->#2` pattern).
8. Hypothesis not falsified: the three survivors are suite artifacts of the id-named sandbox; neutral-sandbox kill rate would be 5/10.
