# T56W2Read01 — cold-read of `## Context gate classification and explicit exit classes — round 15`

- **cand:** `c0137451f5b7f22d65f748fc69f1b181f55e1378` (round-56 C0)
- **heading:** `## Context gate classification and explicit exit classes — round 15`
- **section_sha256:** `132cfb9ef1aa07111af42389e4fe862152e3118b3a8bb66f1d84a6a332e7edf6`
- **section lines at C0:** 1652–1718
- **verdict:** `verified-record` (findings: 0)
- **clone:** `/fast/scratch/hyaku/tameshi-r56/T56W2Read01/clone` (`git clone --shared`, `checkout --detach c0137451f5b7f22d65f748fc69f1b181f55e1378`)
- **receipts:** `.ufo/waves/round-56/w2/T56W2Read01-receipts/commands.txt`, `.ufo/waves/round-56/w2/T56W2Read01-receipts/claims.txt`

## Section identity

Computed with the FROZEN round-18 sectionizer, never reimplemented:

```
python3 - <<'PY'
import importlib.util, subprocess, json
spec = importlib.util.spec_from_file_location("m18", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/measure.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
raw = subprocess.run(["git","-C","/home/vgpnk/Projects/shokunin/tameshi-shokunin","show",
                      "c0137451f5b7f22d65f748fc69f1b181f55e1378:SKILL.md"],
                     capture_output=True, check=True).stdout
for s in m.sectionize(raw):
    if s.get('heading','').strip() == "## Context gate classification and explicit exit classes — round 15":
        print(json.dumps({k: s[k] for k in ('heading','start','end','sha256')}, ensure_ascii=False))
PY
→ {"heading": "## Context gate classification and explicit exit classes — round 15",
   "start": 1652, "end": 1718,
   "sha256": "132cfb9ef1aa07111af42389e4fe862152e3118b3a8bb66f1d84a6a332e7edf6"}
   (64 sections in the file)
```

## Commands I ran (all in the C0 clone)

### 1 — the digests the section names

```
$ sha256sum .ufo/evidence/round-14/capture-context.py
7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89   ← matches the section
$ sha256sum .ufo/evidence/round-14/context-missing-env.json
1ee9d09bc5277fd17b90c7f21e0ed4126825c97875b32b60dfcc2ca2852aa208   ← matches the section
$ sha256sum .ufo/evidence/round-14/context-receipt.json
05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a   ← matches the section
```

### 2 — the maintained gate, in every mode the section's table names

```
$ python3 tools/context-capture.py --check
CONTEXT: OK (id=context_consistent receipt=.ufo/evidence/round-14/context-receipt.json
             sha256=05cb55b8… exit=0 findings=0)
EXIT=0

$ python3 tools/context-capture.py --check \
    --receipt .ufo/evidence/round-14/context-missing-env.json \
    --expected .ufo/evidence/round-15/frozen/context-missing-env/expected.json
CONTEXT: MISMATCH (id=missing_injected_environment … exit=1 findings=2)
FINDING missing_injected_environment receipt.environment.injected_env is absent
FINDING receipt_verdict_mismatch status recorded 'ok' but raw fields recompute 'mismatch'…
EXIT=1

$ python3 tools/context-capture.py --check \
    --receipt .ufo/evidence/round-14/context-receipt.json \
    --expected .ufo/evidence/round-15/frozen/context-clean/expected.json
CONTEXT: OK (id=context_consistent … exit=0 findings=0)
EXIT=0

$ python3 tools/context-capture.py --selftest
…
SELFTEST: PASS (49/49)
EXIT=0

$ python3 tools/context-capture.py --bogus
CONTEXT: USAGE_ERROR (id=usage_error exit=64)
EXIT=64

$ python3 tools/context-capture.py --check --receipt .ufo/evidence/round-14/context-receipt.json
context-capture.py: --receipt and --expected must be given together
CONTEXT: USAGE_ERROR (id=usage_error exit=64)
EXIT=64

$ python3 tools/context-capture.py
context-capture.py: a mode is required
CONTEXT: USAGE_ERROR (id=usage_error exit=64)
EXIT=64
```

Exit-class table of the section vs. observed: `0` clean → observed 0; `1` failed with the stable
ID → observed 1 with id `missing_injected_environment`; `2` could-not-evaluate → observed 2
(`receipt_json_invalid`, `receipt_missing`) on a malformed and on an absent input, with no traceback;
`64` usage → observed 64 on three distinct usage errors. **No command failed.**

### 3 — the section's cited line ranges in the archived script

```
$ sed -n '553,556p;578,580p' .ufo/evidence/round-14/capture-context.py
def decide(receipt):
    comparison = receipt.get("comparison") or {}
    control = receipt.get("positive_control") or {}
    mapping = receipt.get("mapping") or {}
…
    if reasons:
        return "mismatch", 1, reasons
    return "ok", 0, []
$ sed -n '605,606p;641,643p' .ufo/evidence/round-14/capture-context.py
def main(argv):
…
    return code
```

`:2-31` is the module docstring carrying exactly the semantics the section paraphrases (only
top-level `observed_at` excluded, exact environment delta, positive git control, probe/runner
digests against round-13 `expected.json` + `pin-manifest.json`, six leg mappings, 0/1/2/64 map).
The archive byte digest, the two receipt digests, the expected-pin schema
(`tameshi-context-expected-v1`), and the `missing_injected_environment` ID all hold.

### 4 — the "archived, not active" claims

```
$ grep -rn 'capture-context' tools/
tools/context-capture.py:10:gate `.ufo/evidence/round-14/capture-context.py`. It does not capture, does
   (a docstring mention only — no invocation)

$ python3 scan of tools/registry.json
registry rows naming capture-context: []
total registry rows: 57

$ grep -rn 'capture-context' --include=*.py --include=*.sh --include=*.json . | grep -v '^\./\.ufo/'
(no live caller anywhere in the tree)
```

The round-14 table above the section (SKILL.md:1640) carries the archive row
`archived invocation context capture | historical gate, not active | do not run; retained source
.ufo/evidence/round-14/capture-context.py only | … | archive bytes read-only; no supported
invocation`. The section's "not an entry point" and "the maintained gate never invokes it" hold.

### 5 — "read-only inputs, never regenerated"

`tools/context-capture.py` is the only tool that names `.ufo/evidence/round-14/context-receipt.json`
and it opens it read-only. `.ufo/evidence/round-15/verify.py` copies the two round-14 receipts into
its own `.ufo/evidence/round-15/frozen/` tree and asserts `git diff --name-only baseline revision --
.ufo/evidence/round-12 .ufo/evidence/round-13 .ufo/evidence/round-14` is empty
(`historical-evidence-unchanged` PASS in `verification-3.json`). The archived script does carry a
write path to that file (`OUTPUT_REL`, line 58) — which is exactly why the round-14 recipe step 5
above forbids running it. Consistent with the section.

### 6 — "check mode never executes retained argv, never opens a recorded root path"

`run_check()` (1359–1405) contains no subprocess call; the only `subprocess.run` in the tool is
inside the selftest harness (line 1665). The receipt's recorded `lane_root` is only string-validated
(`require_string` / `isabs` / fleet-root-is-parent, lines 517–529), never opened. The selftest's own
`hermetic-no-lane-path` case asserts the live lane root never appears in subprocess output, and
`git status --porcelain` in the clone after every run above is empty.

### 7 — the exit-classes paragraph

The two active gates of the round-15 registry (`retained invocation-context gate`,
`effective expectation disposition`) both carry four codes `0/1/2/64` with `64` mapped to
could-not-evaluate; `tools/evidence-disposition.py:175-178` agrees. "An undeclared nonzero code also
reads as could-not-evaluate" is the `PROTOCOL.md` §Gate standard rule (`PROTOCOL.md:375+`, and
`../PROTOCOL.md` from the lane root resolves to the fleet copy). The claim that the change "changes
no historical command outcome, the round-14 admission, or the C1 scalar" checks out in the diffs:
`0494c24` rewrote the round-14 rows (adding `2 and 64 could-not-evaluate`, replacing the probe
label), `9f2c86f` added the round-15 SCORECARD block whose C1 row reads `6→6, delta0`.

### 8 — the round-15 evidence set at C0 (sweep behind the "effective runtime evidence" sentence)

```
$ for f in verification.json verification-2.json verification-3.json verification-4.json; do … done
verification.json   attempt=—  passed=False failed_checks=['selftest-new','selftest-new-full-count']
verification-2.json attempt=2  passed=False failed_checks=['runner-internal-error']
verification-3.json attempt=3  passed=True  failed_checks=[]
verification-4.json attempt=4  passed=False failed_checks=['tool-source-pin','integrity-tools/mutate-and-run.sh',
                                                           'integrity-SHONEN.md','runner-published-digest','measure-after-fields']

$ git merge-base --is-ancestor 09b5be6… c0137451f5b7f22d65f748fc69f1b181f55e1378 ; echo $?
0        # the commit that added verification-4.json IS an ancestor of C0

$ grep -rn 'verification-4\|attempt-4' SKILL.md LOG.md SCORECARD.md ; echo $?
1        # the later failed receipt is disclosed in no lane document at C0
```

`verification-4.json`'s requested_rev `7c10fa7ba32f` is a descendant of `verification-3.json`'s
`7650fe4db89f`, so it is a much later replay of the round-15 runner against a moved tree, not a
round-15 attempt. Inside it every context-gate check PASSes (`gate-frozen-builtin`, `gate-clean`,
`gate-missing-env`, `gate-tampered-snapshot`, `gate-usage`, `receipt-pin-context-receipt`,
`receipt-pin-context-missing-env`, `integrity-*.ufo/evidence/round-14/*`); its failures are round-15-era
pins re-checked against a tree that had moved.

### 9 — census

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
CENSUS_EXIT=0
```

## Findings

**None.** Every statement in the section is true of the tree at C0 and every command it names runs
as described. Verdict `verified-record`.

## Notes (improvements / stale-but-true / style — not defects)

1. **The effective-evidence pointer is literal but incomplete at C0.** The section says the effective
   runtime evidence is `.ufo/evidence/round-15/verification-3.json` and that "the two earlier failed
   harness receipts remain retained history". At C0 that directory holds **four** receipts, three of
   them failed. `verification-4.json` (attempt 4, `passed=False`) is *not* earlier than
   `verification-3.json`, so the sentence is literally true and `verification-3.json` remains the only
   passing round-15 receipt — but a reader acting on the section at C0 sees three failed receipts in
   that directory and no lane document names the third (`grep` over `SKILL.md`/`LOG.md`/`SCORECARD.md`
   exits 1). Suggested round-57 lesson material: a dated evidence pointer should say how many
   sibling receipts exist and name the later ones, so a cold reader is not left to reconstruct the
   attempt series from the filesystem.
2. The section's own claim that the earlier failures are "not green evidence" is honoured by the
   lane: `LOG.md:975` records `verification.json` as "exited1, not green".
3. "Round-14 receipts are read-only inputs, never regenerated" holds on every active path, but the
   archived script still carries a write path to `.ufo/evidence/round-14/context-receipt.json`
   (`OUTPUT_REL`, line 58). The section and the round-14 recipe step 5 agree that it must not be run;
   a future reader might nonetheless find the `OUTPUT_REL` constant and wonder. A single clause in
   the archive paragraph naming that constant would close the gap.
4. Style: the section repeatedly names `.ufo/evidence/round-15/verification-3.json` in prose; a
   one-clause pointer to the sibling receipts would make the "effective" claim self-evident.

## Files I wrote (nothing else)

- `.ufo/waves/round-56/w2/T56W2Read01.json`
- `.ufo/waves/round-56/w2/T56W2Read01.md`
- `.ufo/waves/round-56/w2/T56W2Read01-receipts/commands.txt`
- `.ufo/waves/round-56/w2/T56W2Read01-receipts/claims.txt`

`SKILL.md` was not edited. No lane production file, no frozen instrument under `.ufo/evidence/`, and
no fleet-root tracked file was touched. Scratch: `/fast/scratch/hyaku/tameshi-r56/T56W2Read01`
(clone only, removed on exit). No git/jj mutation was performed anywhere except a `git clone
--shared` + `checkout --detach` in that scratch directory.
