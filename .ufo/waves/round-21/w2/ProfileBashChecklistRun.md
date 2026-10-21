Verdict: done — the independent F5 observation agrees with the producer for `bash-checklist-run`; I found no actionable defect in this surface.

## Axes

- **Pin identity:** exact repo/revision/path blob and executable mode.
- **Capability:** clean profile actually completes the selftest rather than returning a uniform usage/setup failure.
- **Profile determinism:** exact exit/stdout/stderr tuple across the seven required profiles.
- **Producer consistency:** independently measured tuples compared with the pinned final-production receipt.

## Evidence and result

The frozen contract is `tameshi-shokunin/.ufo/evidence/round-21/c2-contract.json` (lines 9–22: seven profiles, raw tuple definition, and classification rules; lines 27 and 30 pin this surface). The target is `kagi-shokunin/corpus/checklist-run.sh` at `fecee8743e52eb8fb5fbb40782934cb619a1a96e`, not a working-tree substitute. `git cat-file blob REV:path` yielded 24,697 bytes with SHA-256 `7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf`, matching the contract. `git ls-tree` reported mode `100755` and blob OID `78f2c45eed31ee00b01611556affa86a8db9c098`; `git cat-file -s` reported 24697. Each independent per-profile copy preserved that executable bit.

I independently ran each profile from a fresh scratch root with the contracted bubblewrap shape:

```text
bwrap --ro-bind / / --dev /dev --proc /proc --tmpfs /tmp --bind R /tmp/w --unshare-net --die-with-parent --chdir /tmp/w bash /tmp/w/target.sh --selftest
```

The host environment removed every inherited `GIT_*`; clean used only inherited `PATH`, `HOME=/tmp/w/home`, `TMPDIR=/tmp/w/tmp`, `LANG=C`, `LC_ALL=C`, `TZ=UTC`; clean_repeat used a second fresh root; tz, locale, home, and columns applied exactly the contract deltas. All seven subprocesses returned exit 0. Every raw tuple was:

```text
[0,
 b03bc148509bd3ce7e602339c7ffe9103a163c5fba650dea580b98d98bf16611,
 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855]
```

The exact clean stdout was `CHECKLIST_SELFTEST: PASS (34 cases)\n` (36 bytes); stderr was empty (0 bytes). This is a real 34-case selftest pass, not a matching usage/setup response. The source at lines 338–499 shows the selftest fixture construction and final pass/fail count; lines 341–342 create/remove its temporary fixture, line 416 invokes the gate on those fixture files, and lines 493–498 emit the suite result. This path does not write Git state, so fixture Git configuration/private-clone handling was not applicable.

The producer record at `tameshi-shokunin/.ufo/evidence/round-21/f5/receipt-final-production.json` lines 457–530 says `invariant`, `normalization: none`, clean exit 0, and `CHECKLIST_SELFTEST: PASS (34 cases)`. I compared all seven producer tuples, not just the classification: all seven match my independent tuples exactly. Agreement: invariant, no sensitive profiles, clean repeat identical, clean pass 34/34 cases.

The independent run used distinct random scratch-directory names for all profiles. The selftest also uses `mktemp -d` (source line 341), but successful output contains only the fixed case-count summary; no generated path appeared in stdout or stderr. Thus there is no raw random-path variation for this surface. The random-path nondeterminism noted for the separate round-gate surface does not apply here.

## Preserved setup failure

My first scratch materialization wrote the target with the default non-executable mode 0644, contrary to the pinned Git mode 100755. The resulting selftest failed because its child invocations returned 126: outer exit 1, stdout SHA-256 `6431a7bd85cd0d20ca8cecdb29b70f95359f695c7d30081d114345e9fdf57b24`, stderr SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. I preserved this observation in the JSON evidence, corrected the materialization mode, and reran all seven profiles; only the corrected run above is used for the F5 classification. This was harness setup, not a source or producer mismatch.

## Commands / verification record

- `git -C /home/vgpnk/Projects/shokunin/kagi-shokunin rev-parse fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/checklist-run.sh` — exit 0; blob OID `78f2c45eed31ee00b01611556affa86a8db9c098`.
- `git -C /home/vgpnk/Projects/shokunin/kagi-shokunin cat-file blob fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/checklist-run.sh | sha256sum` — exit 0; SHA matches the pin above.
- `git -C /home/vgpnk/Projects/shokunin/kagi-shokunin ls-tree fecee8743e52eb8fb5fbb40782934cb619a1a96e -- corpus/checklist-run.sh` — exit 0; mode 100755.
- `git -C /home/vgpnk/Projects/shokunin/kagi-shokunin cat-file -s fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/checklist-run.sh` — exit 0; 24697 bytes.
- `bwrap --version` — exit 0; bubblewrap 0.13.1.
- Independent corrected seven-profile run — all subprocess exit codes 0, assertions for clean pass, invariant tuples, and exact producer tuple agreement passed.
- No `tools/env-diff.py` invocation/import or helper reuse; no installs/updates; no production files edited.

Independent tuple evidence: `.ufo/waves/round-21/w2/surfaces/bash-checklist-run.json`.

Report: `.ufo/waves/round-21/w2/ProfileBashChecklistRun.md`
