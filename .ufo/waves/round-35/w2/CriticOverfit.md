# CriticOverfit — round 35 wave 2

## Scope, axes, and result

Attacked: the inference that success on the public specimens demonstrates a four-config, full-stdout auditor rather than a lookup table. **Calibration** is the primary impacted axis; **depth** is the capability whose evidence is underdetermined. This is a review, not a claim-admission or Rust-judge decision.

Dispatch revision: `7da6e076c2e25936a3b60dde2a4080d8f05b7e5b`. The assignment's “six public specimens” premise is stale after A4: the committed panel has **eight distinct runner bodies: five kill, three accept**. Both intentionally unsound lookup tools below score all eight correctly against the FIXED apparatus, including its real-root copies. Neither tool executes a runner, enumerates a config, nor compares any runner stdout.

**Ranking:** no CRITICAL against the actual pinned v3 is established by this slice. **BOUND:** public-panel success alone cannot establish the claimed implementation capability. The complete frozen claim is stronger than public success and is not falsified by substituting a different tool in a control experiment. **HYGIENE:** retain the corrected eight-specimen description, not the superseded six-specimen premise.

All experiment files are under `/fast/scratch/hyaku/tameshi-r35-w2/CriticOverfit/`. Source bytes were exported using read-only `git show` at the dispatch revision; no clone, checkout, commit, `.git` write, lane edit, or fleet edit was performed. The only lane file created is this report. The supplied clone/checkout setup was not executed because the canonical bounds prohibit mutating Git operations and writes inside `.git`. No tools installed or updated; no pacman invocation. No default/deciding C1 run or C2 run was invoked.

## BOUND-1 — three hashes suffice to pass every public row

The cheapest demonstrated construction stores only the three accept-body SHA-256s and treats every other input as a runtime failure. This is cheaper than special-casing all eight bodies. The complete 13-line implementation is `/fast/scratch/hyaku/tameshi-r35-w2/CriticOverfit/whitelist.py`:

```python
#!/usr/bin/env python3
import hashlib
from pathlib import Path
import sys
ACCEPT = {
    'b9eb589a3ee01e2f4285f721e2833ed0c5ccbf269e10e8c788da934e93068e2e',
    '5be9b417fcaef014fe53cf57722d2f5dd26afb0637415a4b51704fa59f1b160e',
    '8c654bc71aa5f4877ddec3a52ee458a2af6668aaaacca5f6cc0e812901813b57',
}
passed = hashlib.sha256(Path(sys.argv[2]).read_bytes()).hexdigest() in ACCEPT
print('CHECK runtime ' + ('PASS public-byte-whitelist' if passed else 'FAIL unlisted-byte-default'))
print('TALLY_AUDIT: ' + ('PASS' if passed else 'FAIL'))
sys.exit(0 if passed else 1)
```

A complementary tool, `/fast/scratch/hyaku/tameshi-r35-w2/CriticOverfit/blacklist.py`, stores the five kill-body hashes and accepts everything else. It also gets every public row right. Its default accepts pristine bytes, so the counterexample does not depend on refusing pristine input.

Tool hashes:

- whitelist: `8bdce211ac25625e15df4f49f878aacd6d1df007b11806f7299e0a1866abff6d`
- blacklist: `90ce15cf28f51e38b7ca45a5d3f12b3672e7d97cc2fa733e071a921433fcf680`

### Exact commands and observed exits

Executed through `/fast/scratch/hyaku/tameshi-r35-w2/CriticOverfit/capture.py`, which unsets `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE`, captures full stdout/stderr, and records the child exit without changing it:

```sh
mkdir -p /fast/scratch/hyaku/tameshi-r35-w2/CriticOverfit/control-whitelist-work && python3 /fast/scratch/hyaku/tameshi-r35-w2/CriticOverfit/capture.py /fast/scratch/hyaku/tameshi-r35-w2/CriticOverfit/control-whitelist python3 /fast/scratch/hyaku/tameshi-r35-w2/CriticOverfit/counter.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b --work /fast/scratch/hyaku/tameshi-r35-w2/CriticOverfit/control-whitelist-work --tool /fast/scratch/hyaku/tameshi-r35-w2/CriticOverfit/whitelist.py
mkdir -p /fast/scratch/hyaku/tameshi-r35-w2/CriticOverfit/control-blacklist-work && python3 /fast/scratch/hyaku/tameshi-r35-w2/CriticOverfit/capture.py /fast/scratch/hyaku/tameshi-r35-w2/CriticOverfit/control-blacklist python3 /fast/scratch/hyaku/tameshi-r35-w2/CriticOverfit/counter.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b --work /fast/scratch/hyaku/tameshi-r35-w2/CriticOverfit/control-blacklist-work --tool /fast/scratch/hyaku/tameshi-r35-w2/CriticOverfit/blacklist.py
```

**Both commands exit 1**, not 0. Every public COPY row is `pass=True`; both receipts report:

```text
pub_kill=5/5 pub_accept=3/3 pub_slots=8 pub_distinct=8
ho_kill=0/0 ho_accept=0/0 ho_invalid=0 ho_distinct=0
C1_R35_CONTROL_PASS=false
```

The exit is not suppressed: no held-out copies were supplied, and the complete predicate still requires at least four held-out kills and two held-out accepts (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-35/c1/c1-measure.py:445-449`). **This is a public-panel pass, not a complete C1 pass.** The control's `tool_sha_ok=1` is explicitly permitted by `--tool` (`:365-374`), not a default-mode pin bypass. Its `sealed_after_freeze=1` with no `--sealed` is likewise not an authorship demonstration; the quota conjuncts still fail.

Evidence:

- `/fast/scratch/hyaku/tameshi-r35-w2/CriticOverfit/control-whitelist.{json,stdout,stderr}`; stdout SHA-256 `5707c528045ed85e357aa82bbcb0967fdb09087bd009182bbe9fd8a9cc1c8838`.
- `/fast/scratch/hyaku/tameshi-r35-w2/CriticOverfit/control-blacklist.{json,stdout,stderr}`; stdout SHA-256 `e9267f62f19a0ed16220586626d8f8a63c3f028cf3f0cc1239959835094f9666`.
- Both stderr files are empty, SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

Public body identities, all derived by applying the committed edit triples exactly, are recorded with their source-JSON hashes and exact `git show` commands in `/fast/scratch/hyaku/tameshi-r35-w2/CriticOverfit/inputs.json`:

| Class | Set | Resulting runner SHA-256 |
|---|---|---|
| cfg00-accept-swap | kill | `3b5061b130abc7e07b9a8fbb74e06e98fdf7fcc624316eea16f70a61cd3e189a` |
| cfg11-pass-mask | kill | `b3aaefcdd7a5a7b119982b261500523e7e617e7a7d6a090ce361d6a4d3a495d9` |
| comment-brace | accept | `b9eb589a3ee01e2f4285f721e2833ed0c5ccbf269e10e8c788da934e93068e2e` |
| comment-esac | accept | `5be9b417fcaef014fe53cf57722d2f5dd26afb0637415a4b51704fa59f1b160e` |
| comment-names-leg | accept | `8c654bc71aa5f4877ddec3a52ee458a2af6668aaaacca5f6cc0e812901813b57` |
| root-keyed-auto-mask | kill | `eff823b52779110a7d6e43bb34bbb210b1054aace04bea7e345d13f35647cff2` |
| root-keyed-auto-zero | kill | `62bdbb10ff5fcf05220f4ce21b09e43dc354ad48965ac9ea258e4596c744581f` |
| workdir-branch-swap | kill | `2df05fc3a26ef08ac9dd5914d37020336a53b886c909334b097a7aff5edcdf5e` |

No panel seed is needed: the counter loads sorted committed JSONs at REV (`:248-263,381-384`), and its CLI has no panel-seed argument (`:331-339`). A4's random auto root does not randomize those runner source bytes.

## BOUND-2 — what the sealed set must contain

**Answer:** the sealed scorer defeats the whitelist if it contains even one valid accept whose resulting runner bytes are not one of the three whitelisted bodies. It defeats the blacklist if it contains even one valid kill whose resulting runner bytes are not one of the five blacklisted bodies. These are conditions on **the edited runner bodies**, not filenames, JSON formatting, class names, commit dates, or manifests.

New kill specimens alone cannot defeat default-kill memorization. New accepts alone cannot defeat default-accept memorization. To defeat both demonstrated constructions, the set needs at least one byte-novel valid specimen of each polarity, while retaining the frozen contract's larger minimum of four kills and two accepts. For evidence of the actual capability, the novel kills should include the previously unswept config distinctions and a late-stdout-only difference, rather than only familiar tally mutations.

A5 authenticates committed provenance more strongly, but does not establish cross-public byte novelty. `distinct_bodies` is printed independently for each set; the predicate does not test public/held-out body disjointness (`:321-326,381-384,431-449`). A new JSON committed after the freeze can describe an already-public edited runner body. The acknowledged plain-copy-in provenance limit is explicit in `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-35/contract.json:119`. **[INFERENCE from these source checks]** If a purported sealed set merely reuses the known public runner bodies, its specimen-scoring component will not defeat either decoy. I did not create commits or claim to have passed A5 with such a synthetic history.

### Independent behavioral counterexamples

Command:

```sh
python3 /fast/scratch/hyaku/tameshi-r35-w2/CriticOverfit/capture.py /fast/scratch/hyaku/tameshi-r35-w2/CriticOverfit/probe python3 /fast/scratch/hyaku/tameshi-r35-w2/CriticOverfit/probe.py
```

Observed **exit 0**; `OVERFIT_PROBE: PASS shell_processes=112 comparisons=84`. Full stdout SHA-256 `c06d8259695cb10414bdb486cf1366c5dc5d5d6203030b2374ca518a720dbbf3`; stderr empty. The probe extracts blocks with the frozen counter, not with either lookup tool or v3, then executes each generated Bash driver separately. It compares the actual process exit and **all captured stdout bytes, including the final newline**. No lookup verdict is used as ground truth.

Each fixture is compared with pristine over all four `(auto,KEEP)` pairs and seven vectors: all-zero; one-1; one-2; one-3; one-255; `[1,2,3,255,0,0,0,0,0]`; `[0,3,0,2,0,255,0,1,0]`. Auto roots were generated by the exact command `mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX` (exit 0 twice), not by a fixed literal. Roots were `/tmp/tameshi-r4-2-regression.HXvyp5` and `/tmp/tameshi-r4-2-regression.3PmqcN`; their command-output hashes and every driver command/hash/exit/stdout are in `/fast/scratch/hyaku/tameshi-r35-w2/CriticOverfit/probe-results.json`.

| Fixture | Construction | Observed behavioral differences | Whitelist rc | Blacklist rc |
|---|---|---|---:|---:|
| novel-accept-a | inert full comment after tally's `local nlegs=...` | 0/28 | **1, wrong** | 0 |
| novel-accept-b | inert trailing comment after the `0)` arm | 0/28 | **1, wrong** | 0 |
| novel-kill-stdout-11 | print an extra line on PASS only when auto=1 and KEEP=1 | 1/28: `(1,1)`, all-zero | 1 | **0, wrong** |

The accept constructions change only shell comments; the table is the observed vector coverage, not a claim of exhaustive status-vector execution. These are scratch probes, not purported committed sealed authorship.

Resulting full-runner hashes:

- `/fast/scratch/hyaku/tameshi-r35-w2/CriticOverfit/novel-accept-a.sh`: `36c4fcd3328779cf8cdb0c128ddc15e372a24100c0623d9eede67aa9053b78e8`.
- `/fast/scratch/hyaku/tameshi-r35-w2/CriticOverfit/novel-accept-b.sh`: `a6ab8242a06fae0afa0aca8f392308bdad2bd15694dd151cdd24f68f306c36e4`.
- `/fast/scratch/hyaku/tameshi-r35-w2/CriticOverfit/novel-kill-stdout-11.sh`: `5d0bcc1cdbd243055f4d1541dddf099a58f7246f78193c4e9f246050093437b0`.

Strongest witness: these commands were executed by the probe, and both exit **0**:

```sh
bash /fast/scratch/hyaku/tameshi-r35-w2/CriticOverfit/oracle/pristine-11-zeros.sh
bash /fast/scratch/hyaku/tameshi-r35-w2/CriticOverfit/oracle/novel-kill-stdout-11-11-zeros.sh
```

Pristine stdout (SHA-256 `80822dd6d42bb6cfd1f246e73afbae0f564c3795d14183a626373e4c80b00d8f`):

```text
REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)
REGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.3PmqcN (kept)
```

Copy stdout (SHA-256 `ad8f2f24ea669e5be6e917c78d482bb853c03f91b13b0c2e1e81676521b0c9c9`):

```text
REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)
OVERFIT_EXTRA_STDOUT
REGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.3PmqcN (kept)
```

Driver SHA-256s are respectively `8dc35315864955d661a58929c48059db23975e0952ebce8d92f4071855c49e41` and `aa9bb879f52fccfa6fc91c0718896dfd91af36f62f7e75f40c1eef079362f53d`. The comparison environment and working directory are recorded in `probe-results.json`.

The exact decoy invocations and exits include:

```sh
python3 /fast/scratch/hyaku/tameshi-r35-w2/CriticOverfit/whitelist.py --runner /fast/scratch/hyaku/tameshi-r35-w2/CriticOverfit/novel-accept-a.sh
python3 /fast/scratch/hyaku/tameshi-r35-w2/CriticOverfit/blacklist.py --runner /fast/scratch/hyaku/tameshi-r35-w2/CriticOverfit/novel-kill-stdout-11.sh
```

The first exits **1**, stdout `CHECK runtime FAIL unlisted-byte-default\nTALLY_AUDIT: FAIL\n` (SHA-256 `093f89f5b0cdd0b05cb70a5bd1b06cdf6f4992bd5042ca6ae37a17e8d2097820`). The second exits **0**, stdout `CHECK runtime PASS unlisted-byte-default\nTALLY_AUDIT: PASS\n` (SHA-256 `afdbe445f3db3dbb38df168ad9e8ada7ed27308ce3a60e90652a1077e7bdee24`).

## What this review could NOT break

1. **The actual pinned tool's identity.** Export command `python3 /fast/scratch/hyaku/tameshi-r35-w2/CriticOverfit/prepare.py` exited 0. Its exact read-only Git commands, all exit 0, and source-byte hashes are recorded in `/fast/scratch/hyaku/tameshi-r35-w2/CriticOverfit/inputs.json`:
   - runner: `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`;
   - v3: `ef98fc5367cdb12c71b8b0ddfb5b83835100831f545f6510437dc84014865885`;
   - C1 counter: `515b0b1b00b970f31c08e80eb74512ecae0cf1082ddeccfcb373e810cd0559e8`;
   - contract: `a9eb2b97226ad192352f9da8cc32f3f719db22a93f14355a5e2d1306cea027c0`.
   Both decoys are different bytes. The default counter reads the committed default tool and applies a hash check (`:358,373-374,445`); I did not demonstrate substituting either decoy in deciding mode. The counter's stale internal tool-pin issue is separately owned by CriticPredicate, not counted here as a false-accept.
2. **No actual sealed-set defeat was available at the dispatch pin.** Exact command `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin ls-tree -r --name-only 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b -- /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-35/c1/sealed` exited 0 with empty stdout (SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`). Thus whether the eventual LANDED sealed set defeats the decoys is not measured by this report; the exact necessary distinguishing conditions and working witnesses are above.
3. **The code-level four-config/full-stdout implementation is not refuted by this construction.** `/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/tally-audit-v3.py:349-350` lists all four pairs; `:392-398` retains internal stdout lines; `:401-422` constructs the multi-line oracle; `:544-551` compares each config's tuples. This is source evidence, not an asserted runtime verification of v3. No v3 audit was run by this seat.

## Smallest safe correction

Do not equate public correctness with acquired generalization, and do not weaken or rerun the deciding contract to accommodate the decoys. Keep the runner and tool frozen. Before the single deciding run, ensure the legitimately post-freeze sealed corpus contains byte-novel, independently behavior-validated examples of **both polarities**; include config-specific and late-stdout kill witnesses for the particular capabilities being credited. Record resulting runner digests against public bodies, not merely new JSON names or post-freeze file commits. A no-regression claim over that finite corpus remains a finite-corpus claim, not proof of unrestricted shell equivalence. Any change to a frozen novelty rule belongs to a future contract, not a post-data repair.

## Evidence artifact hashes

Observed command (exit 0): `sha256sum /fast/scratch/hyaku/tameshi-r35-w2/CriticOverfit/prepare.py /fast/scratch/hyaku/tameshi-r35-w2/CriticOverfit/whitelist.py /fast/scratch/hyaku/tameshi-r35-w2/CriticOverfit/blacklist.py /fast/scratch/hyaku/tameshi-r35-w2/CriticOverfit/capture.py /fast/scratch/hyaku/tameshi-r35-w2/CriticOverfit/probe.py /fast/scratch/hyaku/tameshi-r35-w2/CriticOverfit/inputs.json /fast/scratch/hyaku/tameshi-r35-w2/CriticOverfit/probe-results.json /fast/scratch/hyaku/tameshi-r35-w2/CriticOverfit/control-whitelist.stdout /fast/scratch/hyaku/tameshi-r35-w2/CriticOverfit/control-blacklist.stdout /fast/scratch/hyaku/tameshi-r35-w2/CriticOverfit/probe.stdout`.

Additional hashes, all files under `/fast/scratch/hyaku/tameshi-r35-w2/CriticOverfit/`:

| Artifact | SHA-256 |
|---|---|
| prepare.py | `3ab3b9c22521e19066ca9109b9c9b3297a40d9aa828067b655162a7eb9c4dea7` |
| capture.py | `3e20bf7dc25e0d95cd0b5045b5fb92e1962d85d964067c8c154d142735f8346d` |
| probe.py | `8ac1f950d0fb95a19ab4cb7650c43bc344eb7feea568b63d053c801f7914cb7a` |
| inputs.json | `4aae472b90afd53f7e7ac8d67728cba6417427632c66f4d153765b3237a17246` |
| probe-results.json | `5d82941cec2e765a9b2f1238d598d7b59a27773ebbc82241fe7a4af922679f6b` |
