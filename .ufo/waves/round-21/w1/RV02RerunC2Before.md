Verdict: done

## Findings

- The independent C2 count at `33d03b716d3edcf1d8656d46d6df61801d232c52` matches the expected pre-change state in `c2-before.json`: **0/9 classified**, no receipt, no tool/selftest, and no F5 entry. All nine surfaces report `missing-record`; every classification is null. The command's exit **1** is consistent with the counter's contract because the C2 completion conditions are not met.
- All eight surfaces with an explicit `blob_sha256` in `c2-contract.json` resolved through read-only `git cat-file -p`; each computed digest matches its frozen digest. The `tameshi-runner` surface also resolves, and its computed digest is shown below; the contract does not include an expected `blob_sha256` for this surface, so it has no digest comparison to perform.
- The contract and counter SHA-256 values in `c2-before.json` still match the current ruler files. No install/update was performed.

## Counter output and exit

Command:

```text
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/c2-count.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 33d03b716d3edcf1d8656d46d6df61801d232c52 --json
```

Exit: **1** (`echo EXIT=$?` printed `EXIT=1`).

stdout:

```json
{
 "classifications": {
  "bash-checklist-run": null,
  "bash-mado-verify": null,
  "bash-surface-census": null,
  "bash-tsukuroi-census": null,
  "js-claims-check": null,
  "js-kimi-census": null,
  "js-round-gate": null,
  "js-sources-check": null,
  "tameshi-runner": null
 },
 "classified": 0,
 "contract_sha256": "5bd7024d0357ad3fb2a4b8550fd44f8371a3eb004f29948699368bea9d4c2bbd",
 "counter_sha256": "9a34f77d8ae2e219c51c74d60695703ea3efe4f6745ba4b57da2dca2173520a2",
 "f5_entry": false,
 "f5_entry_detail": "entry-missing",
 "receipt_present": false,
 "rev": "33d03b716d3edcf1d8656d46d6df61801d232c52",
 "schema": "tameshi-r21-c2-count-v1",
 "surface_findings": {
  "bash-checklist-run": [
   "missing-record"
  ],
  "bash-mado-verify": [
   "missing-record"
  ],
  "bash-surface-census": [
   "missing-record"
  ],
  "bash-tsukuroi-census": [
   "missing-record"
  ],
  "js-claims-check": [
   "missing-record"
  ],
  "js-kimi-census": [
   "missing-record"
  ],
  "js-round-gate": [
   "missing-record"
  ],
  "js-sources-check": [
   "missing-record"
  ],
  "tameshi-runner": [
   "missing-record"
  ]
 },
 "tool_selftest": {
  "exit": null,
  "present": false
 },
 "total": 9
}
```

stderr summary:

```text
C2: classified=0/9 tool_selftest=fail f5_entry=False rev=33d03b716d3edcf1d8656d46d6df61801d232c52
```

The `tool`, `receipt`, and `entry` paths were each checked at the target revision with `git cat-file -e`; each was absent (exit 128). The target commit resolves (exit 0).

## Frozen pin table

Each row was read with `git -C /home/vgpnk/Projects/shokunin/<repo> cat-file -p '<rev>:<path>'`; all nine object reads exited 0. `computed SHA-256` is over the returned blob bytes.

| Surface | Repo | Revision | Path | Computed SHA-256 | Frozen expected SHA-256 | Result |
|---|---|---|---|---|---|---|
| tameshi-runner | tameshi-shokunin | `08175c62d661fddf052ed10abc91313dec8eb77d` | `tools/mutate-and-run.sh` | `d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b` | not specified | resolved; no expected digest in contract |
| js-kimi-census | kumitate-shokunin | `175de6ba2e9e904010411b19cab27e0af9aad3d4` | `scripts/kimi-census.mjs` | `83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426` | `83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426` | match |
| bash-surface-census | kagi-shokunin | `fecee8743e52eb8fb5fbb40782934cb619a1a96e` | `corpus/surface-census.sh` | `275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f` | `275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f` | match |
| bash-tsukuroi-census | tsukuroi-shokunin | `165307fe4746a8807b02ec4a7d7ecac0368454a6` | `tools/tsukuroi-census.sh` | `084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5` | `084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5` | match |
| bash-mado-verify | mado-shokunin | `eead56b20ad2b28299ae4fa623d52a99b44c743c` | `tools/mado-verify.sh` | `d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13` | `d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13` | match |
| bash-checklist-run | kagi-shokunin | `fecee8743e52eb8fb5fbb40782934cb619a1a96e` | `corpus/checklist-run.sh` | `7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf` | `7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf` | match |
| js-claims-check | kumitate-shokunin | `175de6ba2e9e904010411b19cab27e0af9aad3d4` | `scripts/claims-check.mjs` | `e9a21b441f1216bf41d1cca037b36021c581ec7892df3bf973295f9321b0f61b` | `e9a21b441f1216bf41d1cca037b36021c581ec7892df3bf973295f9321b0f61b` | match |
| js-round-gate | kumitate-shokunin | `364f1d5954158ef8844bca4a5fef57b05d2f2ca5` | `scripts/round-gate.mjs` | `f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9` | `f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9` | match |
| js-sources-check | kumitate-shokunin | `0acb7752d19058b953ebbeba253b1e35f6548de5` | `scripts/sources-check.mjs` | `6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f` | `6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f` | match |

## Baseline comparison and ruler integrity

`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/c2-before.json` records `rev=08175c62d661fddf052ed10abc91313dec8eb77d`, `classified=0`, `total=9`, `receipt_present=false`, `tool_selftest={"exit":null,"present":false}`, and `f5_entry=false` / `entry-missing`; all nine classifications are null and all nine findings are `missing-record`. The rerun at the assigned frozen base has the same C2 state; only the reported revision differs as requested.

| Ruler file | SHA-256 read from file | SHA-256 in c2-before.json | Result |
|---|---|---|---|
| `.ufo/evidence/round-21/c2-contract.json` | `5bd7024d0357ad3fb2a4b8550fd44f8371a3eb004f29948699368bea9d4c2bbd` | `5bd7024d0357ad3fb2a4b8550fd44f8371a3eb004f29948699368bea9d4c2bbd` | match |
| `.ufo/evidence/round-21/c2-count.py` | `9a34f77d8ae2e219c51c74d60695703ea3efe4f6745ba4b57da2dca2173520a2` | `9a34f77d8ae2e219c51c74d60695703ea3efe4f6745ba4b57da2dca2173520a2` | match |

## Evidence paths

- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/c2-count.py`
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/c2-contract.json`
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/c2-before.json`

No additional verification commands or installs were run.