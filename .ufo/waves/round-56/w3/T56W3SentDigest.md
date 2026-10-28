# T56W3SentDigest — receipt-revision-gate: sidecar and ambiguity arms at PIN

Seat: T56W3SentDigest (leaf, wave 3). Judged on: operability. Milestone: sidecar and ambiguity attacks.

## Bottom line

The gate refuses the five literal forms the assignment named, and does so with the named codes. Three of the five answers are not safe as a basis for admission, and the official pipeline makes the weakness worse than the gate's own selftest suggests:

- **Arm 1 (forged sidecar): gate ACCEPTS.** `RECEIPT_DIGEST_MISMATCH` fires only against a stale sidecar. A sidecar rewritten to match tampered bytes passes, and so does a deleted sidecar.
- **Arm 3 (unresolvable control rev) and arm 4 (descendant control rev): the gate refuses only literal lowercase `rev=` tokens.** `controls.sh` `emit()` relabels any rev that does not resolve in the lane as `clone_rev=`, and the gate never reads `clone_rev=`. The official control path therefore cannot trigger these two codes; a control set naming an unresolvable or descendant revision is accepted (E1, E2 below).
- **Arm 2 (two distinct revs): refused, but only for lowercase 7–40-hex tokens.** An uppercase stale token, a 6-char prefix, a 41-char token, or `rev=main` / `rev=HEAD~3` are silently ignored and the receipt passes.
- **Arm 5 (fenced `rev=`): the conflicting-fence case is refused (AMBIGUOUS); a receipt whose only `rev=` sits in a code fence or prose passes**, and so does a fenced required line that contradicts the real verdict value.

The gate's PASS is a weaker statement than its codes suggest. It must not be presented as admission evidence for C2 (see *Residual risk*).

## Setup and provenance (all reads; no lane file written)

- PIN `2f5512a8ab0771fb2eee463ec16db359174f5edd`. Lane HEAD has since moved to `8c20d5c` (one commit, `correct scorecard evidence predicates`); `git diff --quiet PIN HEAD -- tools/receipt-revision-gate.py` is empty, so every result here applies to the gate at HEAD.
- Gate bytes: `git show PIN:tools/receipt-revision-gate.py | sha256sum` = `c60772ceb0ce3f51…`; `git diff --stat 21eb3c63… PIN -- tools/receipt-revision-gate.py` is empty (identical to the frozen instrument).
- `python3 tools/receipt-revision-gate.py --selftest` → `GATE_SELFTEST: 19/19 pass`. **Stale recheck:** `corpus/knowledge/receipt-revision-binding.md` (line 3) states the recheck must print `GATE_SELFTEST: 14/14 pass`; the frozen gate prints 19/19, so that recheck line fails as written. Lane production file; reported, not edited.
- The selftest never exercises a forged sidecar, a fenced `rev=`, uppercase or short tokens, a descendant control (only a sibling, case 9), or the `clone_rev=` relabel.
- Fixtures were built in `mktemp -d` under scratch; the clone `lane4` (`git clone --shared`, `checkout --detach PIN`, one scratch descendant `134bfaf7…`, one scratch sibling `e2c4da53…`) was used only for arms 4 and E3. Scratch was removed at exit. Nothing was committed in the lane. The lane's working tree already carried other seats' uncommitted edits (`corpus/lessons/round-56.md`, `.ufo/evidence/round-21/coldread/…`); not mine, not touched.
- Tools installed or upgraded: none.

Every gate call below prints the gate's own final line. Command template (`G` = lane gate, `L` = lane, `PIN` = `2f5512a8…`, `D` = fixture dir):

    python3 "$L/tools/receipt-revision-gate.py" --lane "$L" --certified "$PIN" --receipt "$D/F:ROLE[:REGEX]"; echo "exit=$?"

## The five assigned arms

| # | Attack (fixture bytes) | Gate final line (verbatim) | Exit | Safe? |
|---|---|---|---|---|
| 1 | Tampered `a1-tamper.txt` (`VERDICT: rev=PIN C1_R56_PASS=true`), sidecar = sha256 of the **tampered** bytes | `GATE: receipts=1 ok=1 refused=0 codes=none verdict=PASS` | 0 | **No** |
| 1b | Same tampered receipt, sidecar left as the honest bytes' digest | `GATE: receipts=1 ok=0 refused=1 codes=RECEIPT_DIGEST_MISMATCH verdict=REFUSED` (`sidecar=883ef30368b6 got=76e5609d29f5`) | 3 | Yes |
| 1c | Tampered receipt, sidecar deleted | `GATE: receipts=1 ok=1 refused=0 codes=none verdict=PASS` | 0 | **No** |
| 2 | `VERDICT: rev=PIN C1_R56_PASS=true` + `STALE rev=C0` (two full tokens) | `GATE: receipts=1 ok=0 refused=1 codes=RECEIPT_REV_AMBIGUOUS verdict=REFUSED` | 3 | Yes (for this form) |
| 3 | `CTL A rev=PIN` + `CTL B rev=deadbeefdeadbeefdeadbeefdeadbeefdeadbeef`, `:control` | `GATE: receipts=1 ok=0 refused=1 codes=RECEIPT_REV_UNRESOLVABLE verdict=REFUSED` | 3 | Yes (literal form only; see E1) |
| 4 | `CTL A rev=<scratch descendant of PIN>`, `:control`, lane = clone | `GATE: receipts=1 ok=0 refused=1 codes=RECEIPT_CONTROL_NOT_ANCESTOR verdict=REFUSED` | 3 | Yes (literal form only; see E2, E3) |
| 5 | ` ```\nrev=C0\n```\nVERDICT: rev=PIN C1_R56_PASS=true` (fence stale + real PIN), `:verdict` | `GATE: receipts=1 ok=0 refused=1 codes=RECEIPT_REV_AMBIGUOUS verdict=REFUSED` | 3 | Yes (conservative; over-refuses) |

## Attack detail

### Arm 1 — forged `.sha256` sidecar

Code path (`tools/receipt-revision-gate.py` lines 114–121): the sidecar is read from `<receipt>.sha256` if present, compared with `sha256(receipt bytes)`, and nothing else. There is no committed digest, no check that the sidecar is a blob, and no requirement that the sidecar exists.

- A1b (stale sidecar): refused, `RECEIPT_DIGEST_MISMATCH` — the only refusal this arm produces.
- A1d (forged sidecar over tampered bytes): **accepted**, `PASS`, exit 0. A sidecar is self-attesting: whoever can write the receipt can write its digest.
- A1c (sidecar deleted): **accepted**, `PASS`. Absence is not an error.
- A1f (sidecar with uppercase hex of the real digest): refused, `RECEIPT_DIGEST_MISMATCH` (`sidecar=76E5609D29F5 got=76e5609d29f5`). Correct for a case-sensitive compare, but a digest written by a tool that uppercases is refused for form, not content.
- A1g / A6b (empty or whitespace-only sidecar): refused, `RECEIPT_DIGEST_MISMATCH`.
- A6a (sidecar path is a directory): **uncaught** `IsADirectoryError` traceback, exit 1, no `GATE:` line. Observed before the fixture was removed. Non-zero, so the deciding run fails closed, but the failure is not a named refusal.

Mitigation that exists: in `deciding-run.sh` lines 117–121 the controls' `.sha256` sidecars are copied with `git show "$REV:…" || exit 2`, so a sidecar missing *from the committed tree* stops the run. That covers only `controls-a` / `controls-b`, and only against removal. A receipt and sidecar rewritten in the same commit pass (A1d equivalent). No out-of-band digest exists to compare against.

### Arm 2 — two distinct `rev=` tokens

- A2a (two full tokens): refused, `RECEIPT_REV_AMBIGUOUS` (`revs=2f5512…,c01374…`).
- A2b (`rev=PIN` and `rev=` 12-char prefix of PIN, same commit): refused `RECEIPT_REV_AMBIGUOUS` — **false refusal** (ambiguity is counted on token text, not on resolved commits).
- A2c (stale `rev=` written **UPPERCASE**): **accepted**, `PASS`, `revs=` shows only the lowercase PIN token. The regex is `[0-9a-f]` and `re.findall` ignores the uppercase token entirely.
- A2f (`rev=PIN0`, 41 hex; `\b` blocks the 40-char match): **accepted** — the token is invisible.
- A2g (`rev=main` baseline line): **accepted**.
- A2h (`rev=c01374`, 6-char stale prefix): **accepted**.
- A2i (`rev=HEAD~3`): **accepted**.
- A2j (control set: `CTL A rev=PIN` + `CTL B rev=c01374`): **accepted**.
- A2e (two `rev=` on one line) and A6c (non-UTF-8 byte beside a second rev): refused, AMBIGUOUS.

Rule the gate actually enforces: the set of tokens matching `\brev=([0-9a-f]{7,40})\b` or `"rev": "…"`, case-sensitive, length 7–40. Everything else is invisible.

### Arm 3 — control naming an unresolvable revision

- A3a (40-hex not in lane): refused, `RECEIPT_REV_UNRESOLVABLE rev=deadbeef…`.
- A3b (12-hex): refused, `RECEIPT_REV_UNRESOLVABLE`.
- A3c (tree id) and A3d (blob id): refused, `RECEIPT_REV_UNRESOLVABLE` — `rev-parse --verify …^{commit}` rejects both.
- **E1 (the official path):** `controls.sh` `emit()` (lines 28–38) runs each `rev=` token through `git rev-parse --verify --quiet <sha>^{commit}` against the lane; a token that does not resolve is rewritten to `clone_rev=`. The gate's `\brev=` regex does not match `clone_rev=` (the `_` is a word character). Result, with the real `emit()` extracted from `controls.sh` and run against the PIN lane:
  - emitted line `CTL CTL_X CTL_X clone_rev=deadbeefdeadbeefdeadbeefdeadbeefdeadbeef fabricated=1`
  - gate on `CTL CTL_P rev=PIN` + that line: `GATE: receipts=1 ok=1 refused=0 codes=none verdict=PASS` (exit 0), `revs=2f5512a8…` only.
  - gate on the emitted line alone: `GATE: receipts=1 ok=0 refused=1 codes=RECEIPT_REV_ABSENT verdict=REFUSED`.
  - So an unresolvable control revision is refused only when it is written by hand, not when produced by the official emitter, and not when mixed with one valid line.

### Arm 4 — control naming a descendant of the certified revision

- A4a (`CTL A rev=<descendant>`, lowercase, clone lane): refused, `RECEIPT_CONTROL_NOT_ANCESTOR rev=134bfaf7…`.
- A4b (PIN + descendant): refused, same code.
- A4c (sibling): refused, same code.
- A4f (a *verdict* naming the descendant): refused, `RECEIPT_REV_MISMATCH`.
- **E2 (official path, PIN lane):** `emit()` with `LANE=PIN lane` on `CTL CTL_D rev=134bfaf7…` → `CTL CTL_D CTL_D clone_rev=134bfaf7… fabricated=1`; combined with `CTL CTL_P rev=PIN`: `GATE: receipts=1 ok=1 refused=0 codes=none verdict=PASS`.
- **E3 (uppercase):** `emit()` on the clone lane (where the descendant *does* resolve) keeps the case: `CTL CTL_U CTL_U rev=134BFAF7222D87E9B65177D5C537D0B59E5EDC42 …`. Combined with `CTL … rev=PIN`: `GATE: receipts=1 ok=1 refused=0 codes=none verdict=PASS`. The lowercase-only gate never sees the descendant. (Control: the same descendant lowercase + PIN is refused, A4b.)
- A4d (ancestor `C0` named by a control, bytes differ at PIN): `GATE: receipts=1 ok=1 refused=0 codes=none verdict=PASS`. This is by design (selftest case 8: "control-ancestors-accepted"): a control set may name any ancestor and is never content-checked. The ER-R54-1 defect class (a positive scored at an older commit) is therefore still open for `role=control`. The deciding run's `controls-b` is `positive` with `--paths`, which does check content; `controls-a` is `control` and does not.

### Arm 5 — `rev=` inside a fenced code block

- A5a (fenced `rev=C0` + real `rev=PIN`): refused, `RECEIPT_REV_AMBIGUOUS`. Safe; over-refuses a receipt that quotes history.
- A5b (real `rev=PIN` + fenced unresolvable): refused, `RECEIPT_REV_UNRESOLVABLE` (over-refuses; fence contents are counted).
- A5c (`rev=PIN` **only** inside a fence; verdict line has no `rev=`): **accepted**, `PASS`. The gate does not bind the rev to the verdict line; any occurrence anywhere in the file counts.
- A5d (`rev=PIN` only in prose): **accepted**, `PASS`.
- A5e (fenced `C1_R56_PASS=true` example; the real verdict line says `C1_R56_PASS=false`; `:verdict:C1_R56_PASS=true`): **accepted**, `PASS`. The required-line check is unanchored substring presence. The deciding run's gate 0c uses `:verdict:C1_R56_PASS=` (key only, any value), so the gate never reads the verdict's value. The value is enforced only by `grep -q "C1_R56_PASS=true"` in `deciding-run.sh`, which is also an unanchored substring grep (`grep -q 'C1_R56_PASS=true' <fixture>` exits 0 on the A5e file).

## Scratch-copy patch (demonstration only; NOT applied to the lane)

The minimal change that closes the token-visibility holes (arms 2, 3, 4 via the emitter) is below. Applied to a scratch copy (`$S/patch/gate.py`), not to `tools/`.

```diff
--- a/tools/receipt-revision-gate.py
+++ b/tools/receipt-revision-gate.py
@@ -40,8 +40,10 @@
-REV_RE = re.compile(r'\brev=([0-9a-f]{7,40})\b')
-JSON_REV_RE = re.compile(r'"rev"\s*:\s*"([0-9a-f]{7,40})"')
+REV_RE = re.compile(r'\brev=([0-9a-fA-F]{7,40})\b')
+JSON_REV_RE = re.compile(r'"rev"\s*:\s*"([0-9a-fA-F]{7,40})"')
+ANY_REV_RE = re.compile(r'\brev=(\S*)')
+CLONE_REV_RE = re.compile(r'\bclone_rev=')
@@ -111,6 +113,11 @@
     revs = sorted(set(REV_RE.findall(text)) | set(JSON_REV_RE.findall(text)))
+    bad = [t for t in ANY_REV_RE.findall(text) if not re.fullmatch(r'[0-9a-fA-F]{7,40}', t.rstrip('.,;:)`\'"*>]}'))]
+    if CLONE_REV_RE.search(text):
+        bad.append('clone_rev')
+    if bad:
+        return ['RECEIPT_REV_UNRESOLVABLE'], 'bad=%s' % ','.join(bad[:3]), None
     sidecar = Path(str(p) + '.sha256')
@@ -137,10 +144,10 @@
     if role_name in ('positive', 'verdict'):
-        if len(revs) > 1:
+        if len(set(resolved.values())) > 1:
             codes.append('RECEIPT_REV_AMBIGUOUS')
             return codes, 'revs=%s' % ','.join(revs), revs
-        full = resolved[revs[0]]
+        full = next(iter(resolved.values()))
```

Scratch evidence for the patch:

- `python3 $S/patch/gate.py --selftest` → `GATE_SELFTEST: 19/19 pass` (unchanged).
- Attack table, original → patched (same fixtures, same lane):

| Attack | Original | Patched |
|---|---|---|
| A1d forged sidecar | PASS | PASS (not addressed) |
| A1e sidecar deleted | PASS | PASS (not addressed) |
| A2a two full revs | AMBIGUOUS | AMBIGUOUS |
| A2b full + 12-char prefix, same commit | AMBIGUOUS | **PASS** (false refusal removed) |
| A2c stale UPPERCASE | PASS | **AMBIGUOUS** |
| A2f 41-char token | PASS | **UNRESOLVABLE** |
| A2g `rev=main` | PASS | **UNRESOLVABLE** |
| A2h 6-char prefix | PASS | **UNRESOLVABLE** |
| A2i `rev=HEAD~3` | PASS | **UNRESOLVABLE** |
| A3a unresolvable 40-hex | UNRESOLVABLE | UNRESOLVABLE |
| A4a descendant (lowercase) | NOT_ANCESTOR | NOT_ANCESTOR |
| A4d ancestor C0 (control) | PASS | PASS (by design, not addressed) |
| A5a fenced stale + real | AMBIGUOUS | AMBIGUOUS |
| A5c rev only in fence | PASS | PASS (not addressed) |
| A5e fenced required line, verdict false | PASS | PASS (not addressed) |
| E1 emitter `clone_rev` unresolvable | PASS | **UNRESOLVABLE** |
| E2 emitter `clone_rev` descendant | PASS | **UNRESOLVABLE** |
| E3 uppercase descendant (clone lane) | PASS | **NOT_ANCESTOR** |
| E3c uppercase descendant in verdict | PASS | **AMBIGUOUS** |

- Regression sweep over the lane's committed-form stdout receipts (`.ufo/evidence/round-53..56` and wave receipts that contain `rev=`; 981 `*.stdout` files, `role=control`, certified PIN): original PASS 264 → patched: **3 newly refused** (`.ufo/waves/round-55/w1/T55W1Er07-receipts/demo-correction-c1.stdout`, `…/T55W1RevQuality-receipts/01-c105-falsifier.stdout`, `.ufo/waves/round-55/w2/T55W2RevNoHarm-receipts/monitor-probes.stdout`); 27 changed ABSENT → UNRESOLVABLE (both refused); **0 REFUSED → PASS**. The round-54/55 real verdict receipts (`round-54/after/c2.stdout`, `round-55/before/c2.stdout`, `round-56/before/c2.stdout`, `round-56/c2/red-before/round-54-ctl-pos-c1.stdout`) remain `RECEIPT_REV_MISMATCH` under both gates. A preliminary version of the patch refused the real `round-55/before/c1.stdout` on a trailing backtick; the final version accepts it.
- A broader sweep over 1291 receipt-like files was started and did not reconcile cleanly (two background runs wrote the same output file); its numbers are not reported here.

What the patch does NOT fix: A1 (sidecar authenticity), A4d (ancestor control by design), A5c / A5e (rev and required line not bound to the verdict line). Those need a design change, not a token fix.

Note on adopting it: `tools/` is the lane's gate, registered against `21eb3c63`, and the deciding run copies the gate from the certified revision. Any patch changes the instrument the deciding run will execute and needs the L1's decision and a successor round; it is not applicable inside round 56 without changing the frozen reference.

## Residual risk the lane must live with

1. **Receipts are not authenticated.** A receipt and its `.sha256` written in one commit pass the gate. The gate proves the receipt *names* a resolvable revision; it does not prove who wrote it or that the run produced it.
2. **Official control revisions are not checked.** `controls.sh` relabels every unresolvable or clone-local revision to `clone_rev=`, which the gate cannot see. For `role=control` (`controls-a`), the binding to the certified revision is therefore nominal: a control set may name revisions the lane does not contain and still PASS. Only `controls-b` (`positive`, `--paths`) is content-checked, and only for the revisions it does name.
3. **Ancestor controls are accepted without a content check** (A4d). The ER-R54-1 class remains open for `controls-a`.
4. **Token grammar is narrow.** Only lowercase 7–40-hex `rev=` tokens and `"rev": "…"` count. Uppercase, short, non-hex, and suffixed names are invisible.
5. **The gate does not evaluate verdicts.** The required line is presence-only and unanchored. It proves a `C1_R56_PASS=` key appears somewhere, not that the verdict is true. The truth check is `grep -q 'C1_R56_PASS=true'` in `deciding-run.sh`, also unanchored.
6. **Operability defects:** the knowledge entry's `14/14` recheck is stale (19/19); a directory sidecar raises an uncaught traceback (exit 1, no named code).

**How the report should state it:** "`receipt-revision-gate.py` at `21eb3c63`/PIN checks that a receipt contains at least one lowercase 7–40-hex `rev=` token that resolves, that it does not name two distinct commits, and (for verdict/positive) that the single named commit matches the certified one or has identical bytes on the declared paths. It does not authenticate receipts (the sidecar is self-attested), does not read `clone_rev=` relabels produced by `controls.sh`, does not check control ancestors' content, does not bind a revision to the verdict line, and does not evaluate verdict values. PASS from this gate is a binding check on names, not evidence that a receipt is authentic or that its verdict is true."

Do not present the C2 operability PASS as admission evidence on the strength of this gate alone. The controls measurement described in the wave brief (the `controls-a` / `controls-b` run and its committed outputs) is the only check on control revisions, and it is itself bounded by the relabel above.

## Commands the deciding run can reproduce (fixture bytes given inline)

Fixture bytes are reproduced from the `printf` calls used; the deciding run needs equivalent committed receipts, not these scratch files.

    PIN=2f5512a8ab0771fb2eee463ec16db359174f5edd
    printf 'VERDICT: rev=%s C1_R56_PASS=true\n' "$PIN" > a1-tamper.txt
    printf '%s\n' "$(sha256sum a1-tamper.txt | sed 's/ .*//')" > a1-tamper.txt.sha256
    python3 tools/receipt-revision-gate.py --lane . --certified "$PIN" --receipt "$PWD/a1-tamper.txt:verdict:C1_R56_PASS=true"
    #  -> GATE: receipts=1 ok=1 refused=0 codes=none verdict=PASS        (forged-sidecar arm; exit 0)

    printf 'CTL A rev=%s\nCTL B rev=deadbeefdeadbeefdeadbeefdeadbeefdeadbeef\n' "$PIN" > a3-ctl-unres.txt
    python3 tools/receipt-revision-gate.py --lane . --certified "$PIN" --receipt "$PWD/a3-ctl-unres.txt:control"
    #  -> GATE: receipts=1 ok=0 refused=1 codes=RECEIPT_REV_UNRESOLVABLE verdict=REFUSED   (exit 3)

    printf 'VERDICT: rev=%s C1_R56_PASS=true\nSTALE rev=%s\n' "$PIN" c0137451f5b7f22d65f748fc69f1b181f55e1378 > a2-two.txt
    python3 tools/receipt-revision-gate.py --lane . --certified "$PIN" --receipt "$PWD/a2-two.txt:verdict"
    #  -> GATE: receipts=1 ok=0 refused=1 codes=RECEIPT_REV_AMBIGUOUS verdict=REFUSED   (exit 3)

    printf 'VERDICT: rev=%s C1_R56_PASS=true\nSTALE rev=%s\n' "$PIN" "$(echo c0137451f5b7f22d65f748fc69f1b181f55e1378 | tr a-f A-F)" > a2-upper.txt
    python3 tools/receipt-revision-gate.py --lane . --certified "$PIN" --receipt "$PWD/a2-upper.txt:verdict"
    #  -> GATE: receipts=1 ok=1 refused=0 codes=none verdict=PASS   (uppercase stale token invisible; exit 0)

Repro of the frozen selftest and the frozen-identity check:

    git show 2f5512a8ab0771fb2eee463ec16db359174f5edd:tools/receipt-revision-gate.py | sha256sum   # c60772ceb0ce3f51…
    python3 tools/receipt-revision-gate.py --selftest | tail -1                                     # GATE_SELFTEST: 19/19 pass

## Not done

- The item's counters (`c1/measure.py`, `c2/measure.py`) were not run; this seat covers only the gate.
- No lane files, frozen instruments, or ledger entries were modified. The patch above is a diff in this report and a scratch-copy demonstration only.
