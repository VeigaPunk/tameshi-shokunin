done

# F5 `bash-surface-census` independent reproduction

**Finding:** No actionable falsification. The producer's `invariant` classification and clean exit are independently reproduced for this pinned surface on the current host. The raw tuple is identical in all seven profiles and matches every producer tuple. This does not claim the skipped handler-verb probes ran.

## Pin and execution

- Current `tameshi-shokunin` `HEAD`: `790abd2129f153c13b471e381d454186edbde65e`.
- Frozen target pin: `c2-contract.json` lines 24–28, specifically line 27: `kagi-shokunin@fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/surface-census.sh`, interpreter `bash`, expected SHA-256 `275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f`.
- Actual commands/results:
  - `git -C /home/vgpnk/Projects/shokunin/kagi-shokunin rev-parse fecee8743e52eb8fb5fbb40782934cb619a1a96e^{commit}` → exit 0; returned the pinned commit.
  - `git -C /home/vgpnk/Projects/shokunin/kagi-shokunin cat-file blob fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/surface-census.sh | sha256sum` → exit 0; SHA-256 exactly `275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f`, 44,212 bytes.
  - `python3 /tmp/tameshi-r21-pbsc/independent-f5.py` → exit 0. This scratch-only harness independently materialised and rechecked the blob, created a fresh `R` with `home/`, `tmp/`, and `target.sh` per profile, and ran `bwrap --ro-bind / / --dev /dev --proc /proc --tmpfs /tmp --bind R /tmp/w --unshare-net --die-with-parent --chdir /tmp/w bash /tmp/w/target.sh --selftest` for each profile. It implemented the profile environments and tuple hashing itself; `tools/env-diff.py` was neither invoked nor imported and none of its helpers were reused.
  - A separate direct clean capture of that same bwrap recipe → exit 0; stdout SHA-256 `09c21ee26b8b8b16618fe68a30043c612811da6bf008840a7a85bd3bce8a2fca`, stderr SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty).
- Runtime observed: bubblewrap 0.13.1, GNU bash 5.3.20, Python 3.14.8, sqlite3 3.54.0.

## Seven-profile raw tuples

Normalization was `none`; each tuple is `(exit, stdout_sha256, stderr_sha256)`.

| Profile | Exit | stdout SHA-256 | stderr SHA-256 |
|---|---:|---|---|
| clean | 0 | `09c21ee26b8b8b16618fe68a30043c612811da6bf008840a7a85bd3bce8a2fca` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| clean_repeat | 0 | `09c21ee26b8b8b16618fe68a30043c612811da6bf008840a7a85bd3bce8a2fca` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| tz | 0 | `09c21ee26b8b8b16618fe68a30043c612811da6bf008840a7a85bd3bce8a2fca` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| locale | 0 | `09c21ee26b8b8b16618fe68a30043c612811da6bf008840a7a85bd3bce8a2fca` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| home | 0 | `09c21ee26b8b8b16618fe68a30043c612811da6bf008840a7a85bd3bce8a2fca` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| columns | 0 | `09c21ee26b8b8b16618fe68a30043c612811da6bf008840a7a85bd3bce8a2fca` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| host | 0 | `09c21ee26b8b8b16618fe68a30043c612811da6bf008840a7a85bd3bce8a2fca` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

So `clean == clean_repeat`, and every profile equals clean: **`invariant`, `sensitive_to: []`** per the frozen rule in `c2-contract.json` lines 19–22. The independent JSON records `tuples_agree: true` for every profile against `.ufo/evidence/round-21/f5/receipt-final-production.json`.

Producer comparison: receipt lines 232–245 pins this same target and says `invariant`, normalization `none`; lines 247–302 report exit 0 and exactly the same stdout/stderr hashes in all seven profiles; line 304 has `sensitive_to: []`. Thus classification, clean exit, and every raw tuple agree (no disagreements).

## Capability and random-path check

The pinned source dispatches `--selftest` at lines 87–100 (line 92), creates a random `mktemp -d` scratch tree at lines 694–698, and emits test outcomes at lines 766–847. The independent clean output ends `SELFTEST: PASS (16 cases)` with exit 0 and empty stderr; it contains 14 actual `ok-case` fixture checks (surface drift/gone/unlisted/link/crosscheck and SQLite/schema/malformed-input paths) and two explicit `skip-case` results for handler verbs. This is real case-by-case test output, not a uniform usage/setup failure.

No random-path variation was observed despite `mktemp -d`: clean and the fresh `clean_repeat` have byte-identical stdout/stderr hashes. A separate full clean stdout capture had zero `/tmp/` occurrences (`grep -c` printed `0`), because successful case output does not include the generated fixture path. The two verb cases skip because `command -v the-janitor` returned status 1 on this host; source lines 817–824 explicitly record both as skips when the handler is absent. This explains the host/clean match here. Residual limitation: those two handler-verb behaviors were not exercised; a host with the handler on `PATH` takes the other branch, so these observations do not establish identical verb capability across hosts.

## Freshness and verification gaps

- Raw-byte SHA-256 of current `c2-contract.json` is `5bd7024d0357ad3fb2a4b8550fd44f8371a3eb004f29948699368bea9d4c2bbd`, equal to the producer receipt's declared contract hash.
- Read-only hash of `790abd2129f153c13b471e381d454186edbde65e:tools/env-diff.py` is `e8b47ab7cf2323764d9e9d3519352cd75e1abda4d5e98e7df602dc23bc099ead`, equal to the producer receipt's declared instrument hash. This is an identity check only; that instrument was not run.
- Independent result: `.ufo/waves/round-21/w2/surfaces/bash-surface-census.json` (12,108 bytes; SHA-256 `f823c2db014cdfb58d4f3f4fe401473c492cd03180bd7395338097d0bf2fbfcb`).
- LSP unavailable: `read xd://lsp` returned “No such tool” and listed mounted devices; no semantic LSP queries were possible. Literal grep was used only to locate source tokens; behavioral conclusions above are from the pinned source and executed profile output, not grep.
- No installs, full batteries, builds, or broad tests were run. This item did not test the env-diff tool's own `--selftest` or the two unavailable handler-verb probes.
