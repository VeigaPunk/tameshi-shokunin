done — T12 genuinely discriminated (frozen ruler: KILLED).

# Scope and axes

- Seat: `TameshiR21.KillT12`; author-side advisory only, not outside admission, integration, or a round-wide judgment.
- Axes: **operability** (the frozen named mutant is runnable and killed by its owning behavioral selftest) and **calibration** (identify the actual discriminator and retain the limits of the observation).
- Measured implementation: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, revision `790abd2129f153c13b471e381d454186edbde65e`.
- Only T12 was probed. No live implementation, contract, ledger, index, ref, corpus, sibling, or runtime-routing edits. No installs or tool updates.

# Mutant and expected detector

Frozen specification `.ufo/evidence/round-21/c1-mutants.json:115-120` replaces the single behavior-bearing assignment at `tools/trace-inputs.py:656`:

```python
# Pristine
                out[path] = sha256_file(path)
# T12
                out[path] = hashlib.sha256(path.encode("utf-8", "surrogateescape")).hexdigest()
```

The defect records the digest of a pathname instead of the opened file's bytes. The frozen ruler observed **anchor_count = 1**. The independent scratch replay also observed exactly one old anchor, and its mutated SHA-256 equals the frozen receipt's mutated SHA-256.

The intended failing case is **`python-read-input`**, `tools/trace-inputs.py:807-810` at the measured revision. Its fixture writes `a.txt` containing `alpha\n` (`:715-723`), launches the public CLI to trace `python3 -c "open('a.txt').read()"`, loads the resulting JSON (`:779-805`), and checks:

```python
rc == 0 and d and d["inputs"].get("a.txt") == hashlib.sha256(b"alpha\n").hexdigest()
```

The expected literal-content digest is `b6a98d9ce9a2d9149288fa3df42d377c3e42737afdcdaf714e33c0a100b51060`. The production helper opens the file in binary mode and hashes its bytes (`tools/trace-inputs.py:501-506`); `run_trace` passes the digests into the JSON input maps (`:651-663`). All source line citations above are to revision `790abd2129f153c13b471e381d454186edbde65e`; the isolated checkout's pristine tool SHA matches the frozen ruler's tool SHA.

# Requested frozen command and actual output

Executed, with inherited `GIT_*` removed from the invoking environment:

```sh
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/c1-survivors.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 790abd2129f153c13b471e381d454186edbde65e --only T12 --jobs 1 --json
```

**Exit: 0.** Full unmodified stdout JSON: `.ufo/waves/round-21/w2/mutations/T12.json`. Full stderr is also saved as `mutations/T12.stderr.txt`; exit as `mutations/T12.exit.txt`.

Actual stderr:

```text
C1 T12 tools/trace-inputs.py KILLED
C1: killed=1 survived=0 inconclusive=0 total=1 rev=790abd2129f153c13b471e381d454186edbde65e
```

| Frozen phase | Exit | Output summary | Failure lines | Timeout |
|---|---:|---|---|---|
| Pristine control | 0 | `SELFTEST: 30/30` | none | false |
| T12 mutant | 1 | `SELFTEST: 29/30` | `FAIL python-read-input` | false |

Both selftest stderr streams were empty. Ruler SHA-256: `a0ec554735b13efa82b5c37534d8beb541204c0f9443d97a040cdd4e248e9396`. Frozen specification SHA-256: `670dd59b9b3d99ec24a6b87aedea531640d4167bb40b2c863066682cf6b3e85c`.

# Same-detector pristine / mutant / restored replay

Because the frozen ruler removes its clones after use (`c1-survivors.py:117-140`), a separate private clone was made at the same revision under:

```text
R=/tmp/tameshi-r21-KillT12-u6x28lu2
D=/tmp/tameshi-r21-KillT12-u6x28lu2/fleet/tameshi-shokunin
```

The clone used the unchanged ruler's `clone` helper (`:60-67`), and read-only sibling access was through symlinks under `R/fleet` inside the ruler's read-only-root bwrap envelope. Only line 656 in this private clone was mutated, then restored. The **unchanged ruler `selftest` function** (`:38-57`) was called for each phase; its subprocess wrapper captured raw outputs without changing argv, environment, or results. Each phase executed this same argv shape (the fully expanded actual argv is preserved for all three phases in `mutations/T12-restoration.json`):

```sh
bwrap --ro-bind / / --dev /dev --proc /proc --tmpfs /tmp --bind "$R" "$R" --unshare-net --die-with-parent --chdir "$D" env -i "PATH=$PATH" "HOME=$R/home" "TMPDIR=$R/tmp" GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 LC_ALL=C python3 "$D/tools/trace-inputs.py" --selftest
```

| Replay phase | Exit | Summary | Exact failed cases | Stderr |
|---|---:|---|---|---|
| Pristine | 0 | `SELFTEST: 30/30` | none | empty |
| T12 | 1 | `SELFTEST: 29/30` | `python-read-input` only | empty |
| Exact-byte restored | 0 | `SELFTEST: 30/30` | none | empty |

Actual changed output lines:

```text
# Pristine
PASS python-read-input
SELFTEST: 30/30
# Mutated
FAIL python-read-input
SELFTEST: 29/30
# Restored
PASS python-read-input
SELFTEST: 30/30
```

All other 29 cases were `PASS` in every phase. Full stdout, stderr, return codes, elapsed times, argv, and output hashes for all phases are preserved in `.ufo/waves/round-21/w2/mutations/T12-restoration.json`. This supplemental replay is restoration evidence, not an additional frozen population count.

# Discriminator assessment and limits

**Genuinely discriminated**, not incidental, equivalent, or inconclusive. The killed case checks the public CLI's runtime output against an independently specified fixture-content digest. It does not inspect, grep, or hash the tool's source to decide its pass/fail. Receipt source hashes are provenance only. The one-line change preserves Python syntax/imports and only replaces the digest calculation; the selftest completes all 30 cases, reports exactly the intended content-digest case as failed, and passes that case again after exact restoration. There is no observed syntax/import exception, outer setup error, timeout, or unrelated assertion failure.

Calibration limit: the aggregate selftest suppresses individual trace-child stderr and deletes individual trace JSON fixtures (`tools/trace-inputs.py:798-805,966`); the raw erroneous per-file digest was not independently retained. The causal attribution rests on the exact one-line semantic mutation, the independent expected-value assertion, the sole named failure, and the reversible same-detector result—not a claim to have inspected a retained failing trace receipt. This kills the frozen T12 path-versus-content mutant; it does not prove exhaustive hashing correctness for all encodings, races, or files.

Witness-hook and registry-PID qualifications are **not applicable to T12**: no malicious-hook execution or real PID reuse was exercised or claimed. Recorded environment/argv pins establish the actual detector invocation contract, not an observation that hostile hooks ran.

Agreement: the requested frozen ruler result is reproducible as a genuine owning-test kill for T12. Disagreement: none within this assigned mutant. No claim is made about the other 17 mutants, round-wide admission, numeric expertise, or unrelated calibration/source re-anchoring.

# Restoration evidence

| Bytes | SHA-256 |
|---|---|
| Pristine private clone | `f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4` |
| T12 private clone | `34db21644cb8e65b5df3908a0bcea72323d3c52240e5bcc69b84cb702bc6b488` |
| Restored private clone | `f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4` |
| Production before and after | `f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4` |

Direct byte equality with the original private-clone bytes was **true before and after the restored detector**. Pristine and restored stdout were exactly equal (SHA-256 `fadbe2c9cb385eb4da8304cc8d1d7b6368bfdde82ee8a920696d23294feffda1`); mutated stdout SHA-256 was `97b5d77c8bff1f4729d65020d6403a3cef46f0630c39cf83a863e3ad44b7f5b7`. Every selftest stderr SHA-256 was the empty-stream digest `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. Production was not mutated.

Report: .ufo/waves/round-21/w2/KillT12.md
