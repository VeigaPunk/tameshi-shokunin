# T48A2RevenNvidiaPair — six-leg flake: is `nvidia-smi` host state the variable?

Seat: revenger, round 48 attempt 2 / w1. Item: attack the competing attribution in
`.ufo/waves/round-48/w1/T48ExecObs2.md` § *Where the six-leg flake lands* — that the tsukuroi leg
“reads live host state (`nvidia-smi` answering)” — by varying **only** `nvidia-smi`.

Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin` read-only; base `473336d9d789f6081195e7376d17836a24666bc3`;
content revision `c7586b9a10effc63b4bd327f976edc094c1bdc17` untouched by this seat. Scratch
`/fast/scratch/hyaku/tameshi-r48/T48A2RevenNvidiaPair` (created, used, removed). No lane file was
written except this report; no git/jj state was mutated (`git show` only, read-only); no package or
tool was installed or upgraded, so the tooling ledger for this seat is empty.

## 0. The object, byte-pinned

The `bash-tsukuroi-census` leg pins a blob, it does not read the fleet work tree:
`tools/mutate-and-run.sh:609-610` `PIN_TSUKUROI=084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5`,
`REV_TSUKUROI=165307fe4746a8807b02ec4a7d7ecac0368454a6`; materialization is
`git show rev:path` (`tools/mutate-and-run.sh:1204`) and the suite is `bash "$MUTANT" --selftest`
(`:1398`). I extracted exactly that blob and verified the pin before running anything:

```
$ git -C …/tsukuroi-shokunin show 165307fe…:tools/tsukuroi-census.sh > census.pinned.sh
$ sha256sum census.pinned.sh
084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5   (976 lines)
```

That is the same blob every wave-1 report on this leg was arguing about (26 selftest cases — the
working-tree census has 121 checks, so the case count alone identifies the pinned blob).

## 1. The required matrix — 6-way, only `nvidia-smi` varied

Runner: 20 invocations per arm, exactly 6 in flight (`xargs -P 6`), each `bash census.pinned.sh
--selftest`, stdout/stderr/rc/duration captured per run. Arms B and C prepend a scratch directory to
the **real** `PATH`, so the host binary stays reachable behind the shim.

| arm | `nvidia-smi` as resolved through `PATH` | runs | rc=0 | failures | failure messages | ms (min–max) |
|---|---|---|---|---|---|---|
| A real PATH (required) | host binary, answering (`NVIDIA GeForce RTX 5070, 615.78.08`, rc 0, 37 ms) | 20 | 20 | **0** | none (stderr 0 B, every line `TSUKUROI_CENSUS_SELFTEST: PASS (26 cases, 26 passed, 0 failed)`) | 4184–7009 |
| B shim exit 1 (required) | `#!/bin/sh` + `exit 1` | 20 | 20 | **0** | none (26/26 PASS ×20) | 4413–5368 |
| C shim hang 1 s (required) | `sleep 1; exit 1` | 20 | 20 | **0** | none (26/26 PASS ×20) | 4166–4849 |
| D tracing shim (added) | logs then `exit 1` | 20 | 20 | **0** | none (26/26 PASS ×20); **0 log lines** | 5598–6136 |
| A′ real PATH, power extension | host binary | +60 | 60 | **0** | none | 4184–9018 (load 84) |

Totals: **140 suite runs, 140 × `PASS (26 cases, 26 passed, 0 failed)`, 0 failures, 0 bytes of
stderr** across all arms. Arm C is decisive on its own: if any case resolved `nvidia-smi` through
`PATH`, the suite would have to absorb ≥22 s of sleep (22 invocations, see §2); the slowest arm-C run
was 4.85 s.

Arm A′ ran under load 84 with a peer seat concurrently exercising the same hard-coded
`/tmp/tsukuroi-r3-2-selftest.XXXXXX` fixture path, so the zero is not an “idle host” artifact: at
10:42:05–10:42:07, with no run of mine in flight, five peer fixture dirs (~1.1 MB each) appeared at
once — the same 6-way shape my own arms used.

## 2. Why `PATH` cannot be the channel (mechanism, byte-pinned)

The pinned selftest never asks `PATH` for `nvidia-smi`. Every case runs the census with an **absolute**
override, and a fixture dispatcher answers it:

| line | fact |
|---|---|
| `:153` | `NVIDIA_SMI=${TSUKUROI_NVIDIA_SMI:-nvidia-smi}` — `PATH` is only the fallback |
| `:630` | `work=$(mktemp -d /tmp/tsukuroi-r3-2-selftest.XXXXXX)` (hard-coded `/tmp`; ignores `TMPDIR`) |
| `:637-686` | fixture dispatcher `.dispatch`, `rc_of`/`out_of` read `$TSUKUROI_FIXTURE` |
| `:680` | `nvidia-smi) out_of smi.out; exit "$(rc_of smi)" ;;` |
| `:688` | `for c in pacman pacman-conf systemctl dmesg journalctl nvidia-smi lsmod; do ln -s .dispatch "$bin/$c"` |
| `:759` | `TSUKUROI_NVIDIA_SMI="$bin/nvidia-smi" \` — passed by `check()` to **every** case |
| `:456`, `:473` | `have "$NVIDIA_SMI"` → `cap … --query-gpu=…` → `if [ "$smi" != ok ]` (the branch the mutant B1 inverts) |

Instrument validation: with the override redirected at the bare name (`TSUKUROI_NVIDIA_SMI="nvidia-smi"`,
equivalently “drop line :759”), the same tracing shim is hit **22 times in one suite run** — so the
shim in arm D was reachable and simply never reached. Under arm D's unmodified override the counter
read 0. `PATH` is inert by construction; host `nvidia-smi` state cannot reach this leg.

## 3. Which attribution the data supports

**Host-state read (“`nvidia-smi` answering”): not supported.** 0 failures in 140 suite runs covering
three different `nvidia-smi` behaviours (answering, failing, hanging), 0 `PATH`-resolved invocations,
no timing signature in the hang arm. The only way to make the pinned leg read a live answer is to
change its bytes at `:759` — which no `PATH`, profile or host state can do. (For completeness: with
the override deliberately removed, the host answer *does* produce the exact wave-1 line — drivers
note `smi=615.78.08`, 22 host calls, +2 s — so host state is a *reachable-if-the-freeze-broke*
producer, not the producer.)

**SIGPIPE race: supported, and it reproduces the exact wave-1 message at the exact case.** The pinned
selftest sets `set -uo pipefail` (`:638`) and asserts with piped `printf | grep -q` at `:771`
(`hostname override not honoured — possible host read`), `:773` (verdict) and `:777` →
`bad … plane evidence missing:$miss` (`:780`). `grep -q` exits on the first match; when the `printf`
side is still scheduled, `pipefail` promotes its 141 to the pipeline status and a *found* match reads
as missing. I built that construct verbatim, against the **real** `out` of the failing case captured
from the pinned blob (872 B, phrase on the 4th of 6 lines, ~200 bytes left to write):

```
$ construct777.sh out.nv.txt 20000     # blob:777 verbatim, re='nvidia-smi not answering'
arm=ambientA iters=20000 false_branches=6 rate=0.0300%   SAMPLE_GOT_CONTAINS_PHRASE=yes
arm=ambientB iters=20000 false_branches=7 rate=0.0350%   SAMPLE_GOT_CONTAINS_PHRASE=yes
```

13 false assertions in 40 000, and **in every one the `got:` string contained the phrase the check
declared missing** — the wave-1 line, from the pinned bytes, with no host involvement. Two peers
already carry the same class from the wild: `T48CritLoad.md:90` (a *received* `plane evidence missing:
'kernel ring unusable'` whose `got:` contains the phrase) and `T48RevenRegression.md` replay B
(`B7: measured=KILLED recorded=SURVIVED` with `hostname override not honoured — possible host read`
on an unrelated case, i.e. a mutant scored red that is textually green).

## 4. Cause or symptom

The failing case message is **only the symptom** — and specifically a **false assertion**. It reports
that the phrase is absent while the very `got:` field printed next to it contains that phrase, so the
line carries no information about the tree, the host or the case's own semantics. It names *which case
lost the race* (whichever `printf | grep -q` site had its `printf` descheduled), and nothing else.
Wave-1 read a host dependency out of that symptom; the dependency is not in the leg.

Two structural consequences, both from the pinned bytes:

1. **No mutant of this spec can produce a one-failure run at this case.** The only defect whose text
   touches the smi branch is B1 (`:473` `smi != ok` → `== ok`); applied, it fails **2** cases
   (`TSUKUROI_CENSUS_SELFTEST: FAIL (26 cases, 24 passed, 2 failed)` — `healthy: nvidia present and
   answering` *and* `blocked: nvidia hardware, driver offline`). A `FAIL (26 cases, 25 passed, 1
   failed)` at that case, as in wave-1's P1, is therefore not a stray mutant either — it is the
   scheduler.
2. **Wave-1's evidence cannot discriminate its own claim.** The two producers leave different
   fingerprints inside the printers' `got:` string: a live host read writes `smi=<driver version>`
   (probe: `smi=615.78.08`) and costs ~+2 s; a SIGPIPE false assertion writes the fixture's
   `smi=rc=6` and costs nothing. Wave-1's quote is truncated exactly at `backup_diffs=…`, i.e. before
   the drivers plane — the one field that separates the two attributions. Its conclusion is not
   supported by the evidence it preserved, and its own control duration (7218 ms) sits between my
   fixtures (4600 ms) and my host-read probe (6635 ms), i.e. it does not discriminate either.

## 5. Feeds for C1 (calibration)

- Do **not** put a host/nvidia dependence in the row for `six-leg regression ledger`: with the freeze
  intact the leg is invariant to `nvidia-smi`, measured three ways (140/140). Adding `nvidia` (or any
  host-state name) to `deps` would assert a dependence that does not exist.
- The class stays `nondeterministic` for the scheduling reason the peers receipted
  (`{PASS passed=9 | 0, FAIL passed=8 | 1}`, and a `SETUP` face when the race lands on the control run:
  `CONTROL: RED` → sweep refuses at `tools/mutate-and-run.sh:533`).
- Signature to read before scoring a mismatch at the deciding run: in
  `…/regression-wd/bash-tsukuroi-census/evidence/control.out`, `plane evidence missing: '<phrase>'`
  or `hostname override not honoured` **whose `got:` contains the phrase** is the race, not the tree;
  `smi=<version>` in the drivers plane would be the (much rarer) freeze-breach face.

## 6. Limits

- `[O]` Everything numeric above: pin hash, 140/140 arm results with per-run rc and durations, the
  0-vs-22 invocation counts, the 13/40 000 construct false assertions with `SAMPLE_GOT_CONTAINS_PHRASE=yes`,
  probe-C/B1 counts, line numbers.
- `[I]` That the wave-1 P1 control red is the SIGPIPE face rather than a freeze breach: its preserved
  text omits the discriminator (§4.2). What is measured is that host-state variation reproduces
  nothing (0/140) while the race reproduces the identical line (13/40 000).
- One host, load 10–84, one blob; no organic full-suite hit in my 140 runs (the race is rare per site,
  ~0.03 % here), so the arm counts bound “host state is not the variable”, not “the race fires at
  rate r”.
- The selftest writes to `/tmp` by hard-coded template (`:630`), ~1.1 MB per run, outside `TMPDIR`;
  that is a property of the pinned fleet file, not of this lane, and was not edited. The
  `/tmp/tsukuroi-r3-2-selftest.*` dirs seen during my arms are a concurrent peer's (5 born at
  10:42:05–10:42:07 with no run of mine in flight), not mine, and were left alone; my own arms' traps
  removed their directories (0 of my 140 runs left a dir behind).
