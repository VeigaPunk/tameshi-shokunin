# Mutkillvectorfailthreshold — round-34 w1 mutation probe

Seat: mutation-tester (leaf, no dispatch). Claim under attack: C1 (operability capability
acquisition, `tools/tally-audit-v2.py`) MEASURED TRUE at revision
`c17e593b51802dd4ed568da3265f21c6d00c4273`, per the deciding-run receipt
`.ufo/evidence/round-34/measure/c1-deciding-run.stdout` (sha256 `3e28149f94f2e5d832e680285306f0166029858982cfc5ae32bd4f19c9a9b05c`, exit file
`c1-deciding-run.exit` = `0`, sha256 `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa`), which reports `ho_kill=8/8 ho_accept=6/6
ho_invalid=0 … C1_R33_PASS=true`. Lane tip at dispatch:
`0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`.

Scratch root (all writes here, plus this one report):
`/fast/scratch/hyaku/tameshi-r34-seats/Mutkillvectorfailthreshold/`.
Kill rule consumed: the counter CLI was never run in default mode; the counter was imported as a
module in the scratch dir and only its functions (`validate_ho`, `apply_edits`, `tally_block_of`,
`block_run`, `ho_witness_ok`, `run_tool_sandboxed`, `bwrap_argv`) were called on scratch copies.

## 1. Setup and pin verification (before any run)

```console
$ mkdir -p /fast/scratch/hyaku/tameshi-r34-seats/Mutkillvectorfailthreshold && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r34-seats/Mutkillvectorfailthreshold/lane; echo clone_rc=$?
clone_rc=0
$ env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C lane checkout -q --detach 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7; echo checkout_rc=$?
checkout_rc=0
$ env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C lane rev-parse HEAD
0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7
$ env … git -C lane show 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7:tools/tally-audit-v2.py > tool.py; echo tool_extract_rc=$?
tool_extract_rc=0
$ env … git -C lane show 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7:tools/mutate-and-run.sh > pristine.sh; echo runner_extract_rc=$?
runner_extract_rc=0
$ sha256sum tool.py pristine.sh
7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10  tool.py
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  pristine.sh
```

Both match the frozen pins exactly. The sealed copy's bytes at the fleet path equal the blob at the
tip (`git show 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7:.ufo/evidence/round-33/heldout/ho-kill-vector-fail-threshold.json |
sha256sum` → `5d8cea2eddafc49e76ada954a1e6cf0b6d69f509f4f90838b6561e97a47a9c43`, identical to the working-tree file). Counter pin
`sha256(lane/.ufo/evidence/round-33/c1/c1-measure.py)` = `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c`, matching the amendment-6
freeze pin.

Detector (identical for pristine, mutated and restored bytes): the frozen counter's
`run_tool_sandboxed(tool, copy, work)` — real `python3 -I /w/tool.py --runner /w/copy.sh` under
`bwrap` with `timeout` outside the sandbox — plus a supplementary identical `bwrap` argv capture for
the full `CHECK` lines. Tool bytes in every run were `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` (recorded per run in
`results/*.json`).

## 2. Sealed copy: mutation, witness, verdict

The JSON's single edit (old string occurs exactly once in the tip bytes — asserted by
`apply_edits`; `prep.json` `old_count_in_pristine=1`):

```
-old  "  if [[ $nfail -gt 0 ]]; then\n"
+new  "  if [[ $nfail -gt 1 ]]; then\n"
```

Built with the counter's own `apply_edits` → `copies/sealed-ho-kill-vector-fail-threshold.sh`,
sha256 `17496eb0f27dd0c4593ec1c94b655f6335f278b2c5885aa3ebbfa8e362fcdb7e`. The sealed JSON file
itself is `5d8cea2eddafc49e76ada954a1e6cf0b6d69f509f4f90838b6561e97a47a9c43`.

Witness (counter functions on scratch copies, `prep.py` rc 0, `prep.json` sha256 `c554ecdca73a7bcb4efa8d4c9065d1d2ea8e741bdd729579a8b43609dd5b0de9`):

```console
sealed witness True vector
  a (pristine block, vec [1,0,0,0,0,0,0,0,0]) = (1, 'REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)')
  b (mutant block,   vec [1,0,0,0,0,0,0,0,0]) = (0, 'REGRESSION: PASS (cases=9 passed=8; ledger legs exact: killed-delta<=0 flips<=0)')
```

Same detector, three byte states (commands in §6; wrapper exit files `results/sealed-rc.toolrun.exit`
= 0, `results/restored.json` run rc 0):

| bytes | copy sha256 | tool outcome | rc | last line |
|---|---|---|---|---|
| pristine `pristine.sh` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | ACCEPT | 0 | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` |
| sealed mutant | `17496eb0f27dd0c4593ec1c94b655f6335f278b2c5885aa3ebbfa8e362fcdb7e` | **KILL** | **1** | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)` |
| restored (`copies/restored.sh` = pristine bytes) | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | ACCEPT | 0 | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` |

The kill was earned on the intended surface, not incidentally:
`CHECK runtime FAIL vectors=15158 mismatched=1638; first: cfg(0,1) statuses 1 0 0 0 0 0 0 0 0: got
(0, 'REGRESSION: PASS …'), want (1, 'REGRESSION: FAIL …')` (`logs/sealed-rc.log`). Head, static and
harness all PASS. **Verdict for the assigned copy: KILLED, as its label demands.** The deciding
receipt's `ho_kill=8/8` is consistent with this copy.

Restoration: `copies/restored.sh` rebuilt from `pristine.sh` after the mutant runs is byte-identical
(`a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`) and re-audits ACCEPT; `pristine.sh` and `tool.py` shas are unchanged, lane
`git status --porcelain` is empty and HEAD is still `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`. Nothing in the fleet tree or lane
was written.

## 3. Adversarial: a witness-valid, tool-ACCEPTED construction — CRITICAL (witness gate, not tool)

### 3.1 Why a plausible in-family construction cannot survive

The witness vector is itself in the tool's oracle sweep. `ho_witness_ok` for a kill+vector copy
requires `pb != mb` and `block_run(pb, vec) != block_run(mb, vec)` at the declared vector
(`c1-measure.py:206-218`; `block_run` compares `(rc, first stdout line)` under a fixed shim,
`c1-measure.py:154-176`). `tally-audit-v2.py`'s runtime check sweeps every status 0..255 at every
leg position — including vector `[1,0,…,0]` — under two configs, against an oracle of the pristine
semantics (`tool.py:265`, `tool.py:381`, `tool.py:290-302`, `tool.py:372-438`). Therefore any
divergence that is a function of the status vector alone, visible at the witness vector, necessarily
makes the tool's runtime check fail; the tool's label then equals the witness-set label.

Measured, all five plausible in-family constructions (status-only weakenings of the FAIL gate,
including the sealed copy) were witness-valid **and** killed:

| variant | construction | witness | tool outcome | runtime mismatches |
|---|---|---|---|---|
| sealed copy | `[[ $nfail -gt 1 ]]` | True `vector` | KILL rc=1 | 1638 |
| `adv-ge2` (`copies/adv-ge2.sh`, `b7e264e58d640b0ebcf6cfb82adae0d67c46dd75b62efb33efcd3808fb565123`) | `[[ $nfail -ge 2 ]]` | True `vector` | KILL rc=1 | 1638 |
| `adv-arith-gt` (`b15f961fd3fde6d5424e146e3cdd9f4cf5a7716a0b93f4a5083f59d19af8ae33`) | `(( nfail > 1 ))` | True `vector` | KILL rc=1 | 1638 |
| `adv-pass-count` (`4cc1eadd44e002aa717a3bdf8000c314d4264ba853f1a634e40dd0d25e84eda4`) | `[[ $nfail -gt 0 && $npass -lt $((nlegs - 1)) ]]` | True `vector` | KILL rc=1 | 20 |
| `adv-arm-reset` (`7250288605cf0113049e8c77f0341534360724a73eb1141c672aaf62aa80d5e1`) | `1) nfail=$((nfail + 1)); if (( nfail == 1 )); then nfail=0; fi ;;` | True `vector` | KILL rc=1 | 1800 |

So within the *shim-insensitive* family, no surviving construction exists; the proof above is
confirmed by these five runs (`results/adv-ge2.json`, `adv-arith-gt.json`, `adv-pass-count.json`,
`adv-arm-reset.json`; `logs/*.log`).

### 3.2 Construction that satisfies the attack criterion

The escape must depend on a value that differs between the witness shim and **both** audit configs.
The witness shim is `root=r auto=0 KEEP=1` (`c1-measure.py:167`) and its environment is *empty*:
`block_run` passes `env={'PATH','HOME','TMPDIR','LC_ALL'}` to `bwrap`, but `bwrap --clearenv`
(`c1-measure.py:229`) drops it. Reproduced exactly:

```console
$ env -i PATH=/usr/bin:/bin HOME=/w TMPDIR=/tmp LC_ALL=C bwrap --unshare-all --die-with-parent --new-session --clearenv --dev /dev --proc /proc --tmpfs /tmp --ro-bind /usr /usr --ro-bind /bin /bin --ro-bind /lib /lib --ro-bind /lib64 /lib64 --ro-bind /etc /etc --bind "$PWD/envprobe" /w --chdir /w /usr/bin/env; echo exact_probe_rc=$?
PWD=/w
exact_probe_rc=0
```

The tool's audit, by contrast, runs `bash` directly with `root` in `{'tally-audit',
'/tmp/tally-audit-work'}`, `HOME=<tmp>`, `TMPDIR=<tmp>`, `LC_ALL=C` (`tool.py:265`, `tool.py:253-262`).
Two constructions were built, both from the pinned pristine bytes with the counter's `apply_edits`
(old string count == 1), both `validate_ho`-clean, both **witness-valid (`True, 'vector'`)** and both
**labelled by the real pinned tool `TALLY_AUDIT: PASS`** — opposite to their witness-set (`kill`):

**Finding A — shim-variable channel.** Exact JSON (`copies/adv-witness-shim-root.json`, sha256
`1461e20fc3ea9fe5807648c026eda8a42fbc3ef737c1408e4557d56350e634da`; mutant bytes `copies/adv-witness-shim-root.sh`, sha256 `24fabbeab72e9edd1ace4ee7631effba14665a98947697c5bfbbab00003d15e1`):

```json
{
 "id": "adv-witness-shim-root",
 "author": "Muskillvectorfailthreshold seat r34",
 "set": "kill",
 "edits": [
  {
   "old": "  if [[ $nfail -gt 0 ]]; then\n",
   "new": "  if [[ $nfail -gt 0 && $root != r ]]; then\n"
  }
 ],
 "witness": {
  "vector": [1, 0, 0, 0, 0, 0, 0, 0, 0]
 }
}
```

Observed: witness `True vector`; `a = (1, 'REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)')`,
`b = (0, 'REGRESSION: PASS (cases=9 passed=8; ledger legs exact: killed-delta<=0 flips<=0)')`; tool
`ACCEPT`, rc 0, `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)`,
`runtime vectors=15158 mismatched=0`, `harness faults rejected=34/34`
(`logs/adv-witness-shim-root-rc.log`, `results/adv-witness-shim-root.json`).

**Finding B — witness-environment channel.** Exact JSON (`copies/adv-witness-env-home.json`, sha256
`0dbb73cfc4e57d24a9b1ffe01d5ae3ed3e95d674683a10b9e830fc52c1f506b3`; mutant bytes `abcd9585733123c69fdf0413b031127b97c9e3debec7264f386afc1d0bdce77a`):

```json
{
 "id": "adv-witness-env-home",
 "author": "Muskillvectorfailthreshold seat r34",
 "set": "kill",
 "edits": [
  {
   "old": "  if [[ $nfail -gt 0 ]]; then\n",
   "new": "  if [[ $nfail -gt 0 && $HOME != /w ]]; then\n"
  }
 ],
 "witness": {
  "vector": [1, 0, 0, 0, 0, 0, 0, 0, 0]
 }
}
```

Observed: witness `True vector`; `a = (1, 'REGRESSION: FAIL …')`, `b = (1, '')` — under `set -u` the
unset `HOME` aborts the witness run, and the witness compares only `(rc, first line)`, so the crash
counts as a demonstrated fault; tool `ACCEPT`, rc 0, `TALLY_AUDIT: PASS (head=pass static=pass
runtime=pass harness=pass)`, mismatched=0 (`logs/adv-witness-env-home-rc.log`,
`results/adv-witness-env-home.json`). This variant is a witness-only difference in the strictest
sense: in any environment where `HOME` is set, its logic is the pristine logic.

### 3.3 Impact and boundary

- The amended `ho_witness_ok` does not establish that a kill copy is a real defect; it establishes
  that the copy's block behaves differently **under its own fixed shim**. Both constructions above
  are blameless under the tool's audit (and under a real `--regression` run: `root` is a `/tmp`
  path, `HOME` is set) and defective only at the witness values.
- If either were sealed as `must-kill`, the counter's held-out loop would count it
  (`ho_kt += 1`, `c1-measure.py:403`) and the tool would not kill it (`ho_k += 0`,
  `c1-measure.py:420`), so `ho_kill == ho_kt` would fail and C1 would be recorded false. The gate
  cannot reject witness-targeted copies.
- This does **not** prove any landed artifact wrong: the assigned sealed copy is genuinely killed
  (§2), all eight sealed kills stood in the deciding run, and the deciding receipt stands as an
  observation. The seam is a coverage finding against the witness gate, routed for the next wave —
  e.g. witness `block_run` should use the tool's `(root, auto, KEEP)` triples and an explicitly set
  environment (`--setenv`, not an env dict that `--clearenv` discards), and/or require the
  divergence to persist under a second config. No edits were made this wave (frozen artifacts).

## 4. Tooling

No installs or upgrades: bwrap 0.13.1, Python 3.14.8, coreutils, git were already present and
sufficient. No pacman transactions.

## 5. Files (all in scratch)

- `prep.py`, `toolrun.py`, `prep.json` (`c554ecdca73a7bcb4efa8d4c9065d1d2ea8e741bdd729579a8b43609dd5b0de9`) — build/witness and detector wrappers.
- `copies/*.sh`, `copies/*.json`, `results/*.json`, `results/*.toolrun.exit`, `logs/*.log`,
  `envprobe/block_run_env.txt` — the evidence quoted above; each run's copy and tool sha256 are in
  its `results/*.json`.

## 6. Reproduce

```console
S=/fast/scratch/hyaku/tameshi-r34-seats/Mutkillvectorfailthreshold
python3 $S/prep.py; echo prep_rc=$?                                  # -> 0, prep.json
python3 $S/toolrun.py $S/pristine.sh $S/results/baseline.json baseline; echo rc=$?          # ACCEPT rc=0
python3 $S/toolrun.py $S/copies/sealed-ho-kill-vector-fail-threshold.sh \
        $S/results/sealed-rc.json sealed-rc; echo $? > $S/results/sealed-rc.toolrun.exit    # KILL rc=1
python3 $S/toolrun.py $S/copies/adv-witness-shim-root.sh \
        $S/results/adv-witness-shim-root-rc.json adv-witness-shim-root-rc; echo $? > $S/results/adv-witness-shim-root-rc.toolrun.exit   # ACCEPT rc=0
python3 $S/toolrun.py $S/copies/adv-witness-env-home.sh \
        $S/results/adv-witness-env-home-rc.json adv-witness-env-home-rc; echo $? > $S/results/adv-witness-env-home-rc.toolrun.exit     # ACCEPT rc=0
python3 $S/toolrun.py $S/copies/restored.sh $S/results/restored.json restored; echo rc=$?  # ACCEPT rc=0
```

The variants are rebuilt from the pinned `pristine.sh` by the counter's own `apply_edits` in
`prep.py`; the exact edit strings and witness vectors are the JSON in §3.2.

## 7. Verdict summary

| item | expected | actual | verdict |
|---|---|---|---|
| sealed `ho-kill-vector-fail-threshold` (kill) | rc 1, `TALLY_AUDIT: FAIL` | rc 1, `TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)`, 1638 runtime mismatches | **KILLED** |
| pristine / restored bytes | rc 0, `TALLY_AUDIT: PASS` | rc 0, `TALLY_AUDIT: PASS`, mismatched=0 | baseline green, restore exact (`a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`) |
| plausible in-family variants (4) | KILL | KILL ×4 | no survivor |
| witness-shim/env-targeted variants (2) | (attack) | witness True `vector`, tool ACCEPT rc 0 | **witness-gate seam — critical finding, exact JSON in §3.2** |
