# T56W3CritCopiedRev — C2 copied-`rev=` attack (operability)

Seat: T56W3CritCopiedRev · L1: TameshiR56a3 · Lane: /home/vgpnk/Projects/shokunin/tameshi-shokunin
Certified revision: `2f5512a8ab0771fb2eee463ec16db359174f5edd` (PIN) · C0 `c0137451f5b7f22d65f748fc69f1b181f55e1378`
Gate: `tools/receipt-revision-gate.py` (read-only; git objects and the receipt bytes only)
Tools installed: none. No lane file, frozen instrument, or ledger was modified. Scratch was `$HYAKU_SCRATCH/tameshi-r56/T56W3CritCopiedRev` and was removed on exit; every fixture is reproducible from the commands below with `S=$(mktemp -d)`.

## Verdict

**The copied-`rev=` attack passes the gate.** A receipt whose only binding content is `rev=<certified>` and whose verdict line is a fabricated `C1_R56_PASS=true C2_R56_PASS=true` is accepted as `verdict=PASS` with `exit=0`. The `.sha256` sidecar does not stop it when the forger writes the sidecar too. `--paths` does not stop it, because `--paths` is consulted only when the receipt's `rev` differs from the certified revision.

The round's `cannot_see` sentence is accurate for the copied-rev case. It is incomplete: the gate also cannot see the verdict's contents, whether the receipt was produced by any run, and whether a receipt is tracked by git. Details below.

## What the gate checks (from source)

`check()` in `tools/receipt-revision-gate.py` tests, in order:

1. the path exists, is a regular file, and is non-empty;
2. if `<receipt>.sha256` exists, its first token equals the sha256 of the receipt bytes (`RECEIPT_DIGEST_MISMATCH`);
3. if a REGEX is given, it matches somewhere in the text (`RECEIPT_REQUIRED_LINE_MISSING`);
4. at least one `rev=<hex7-40>` or JSON `"rev": "<hex>"` token exists (`RECEIPT_REV_ABSENT`), each resolves (`RECEIPT_REV_UNRESOLVABLE`);
5. for `positive`/`verdict`: exactly one distinct rev (`RECEIPT_REV_AMBIGUOUS`); it equals the certified commit, or, only when `--paths` is given, the listed paths have identical bytes at both commits (`RECEIPT_REV_MISMATCH` / `RECEIPT_REV_CONTENT_DRIFT`).

The gate never parses `C*_PASS=` values, never checks whether the file is tracked or committed, and never checks that any counter, control script, or run produced the text. The source says so in a comment at line 109: "only size/type sanity is possible here". Passing the digest check does not establish provenance.

## Commands and outputs

All commands use `L=/home/vgpnk/Projects/shokunin/tameshi-shokunin`, `G=$L/tools/receipt-revision-gate.py`, `R=2f5512a8ab0771fb2eee463ec16db359174f5edd`, and `S` as a scratch directory. The lane resolved as expected: `git -C "$L" rev-parse --verify --quiet "$R^{commit}"` printed `2f5512a8ab0771fb2eee463ec16db359174f5edd`, and `git -C "$L" rev-parse --show-toplevel` printed `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.

**A. Copied rev token plus fake verdict, no sidecar, no paths** (the core demonstration)

```
printf 'VERDICT: rev=%s C1_R56_PASS=true C2_R56_PASS=true\n' "$R" > "$S/fake-verdict.txt"
python3 "$G" --lane "$L" --certified "$R" --receipt "$S/fake-verdict.txt:verdict"; echo "exit=$?"
GATE OK .../fake-verdict.txt role=verdict revs=2f5512a8ab0771fb2eee463ec16db359174f5edd
GATE: receipts=1 ok=1 refused=0 codes=none verdict=PASS
exit=0
```

**B. Same, plus a regex requiring the verdict line**

```
--receipt "$S/fake-verdict.txt:verdict:C2_R56_PASS=true"
GATE OK ... revs=2f5512a8ab0771fb2eee463ec16db359174f5edd
GATE: receipts=1 ok=1 refused=0 codes=none verdict=PASS
exit=0
```

**C. Forger writes a matching `.sha256` sidecar** (`sha256sum fake-verdict.txt > fake-verdict.txt.sha256`)

```
GATE OK ... revs=2f5512a8ab0771fb2eee463ec16db359174f5edd
GATE: receipts=1 ok=1 refused=0 codes=none verdict=PASS
exit=0
```

**D. Sidecar control: receipt edited after its sidecar was written**

```
printf 'VERDICT: rev=%s C1_R56_PASS=true C2_R56_PASS=true (edited)\n' "$R" > "$S/edited.txt"
cp "$S/fake-verdict.txt.sha256" "$S/edited.txt.sha256"
GATE REFUSED ... code=RECEIPT_DIGEST_MISMATCH sidecar=29adecba38f9 got=3d773d3b2f4b
GATE: receipts=1 ok=0 refused=1 codes=RECEIPT_DIGEST_MISMATCH verdict=REFUSED
exit=3
```

The sidecar catches a mismatch between an edited receipt and a stale sidecar. It does not catch a receipt and sidecar written together.

**E. Sidecar plus `--paths` (frozen surface), rev equal to certified**

```
printf '.ufo/evidence/round-56/contract.json\n' > "$S/paths.txt"
python3 "$G" --lane "$L" --certified "$R" --paths "$S/paths.txt" --receipt "$S/fake-verdict.txt:verdict"
GATE OK ... revs=2f5512a8ab0771fb2eee463ec16db359174f5edd
GATE: receipts=1 ok=1 refused=0 codes=none verdict=PASS
exit=0
```

`--paths` is not consulted when the revision equals the certified one, so it cannot stop this.

**F. Negative control: honest rev token for C0, no paths**

```
printf 'VERDICT: rev=%s C1_R56_PASS=true\n' "$C0" > "$S/c0-verdict.txt"
GATE REFUSED ... revs=c0137451f5b7f22d65f748fc69f1b181f55e1378 code=RECEIPT_REV_MISMATCH rev=c0137451f5b7f22d65f748fc69f1b181f55e1378 certified=2f5512a8ab07
GATE: receipts=1 ok=0 refused=1 codes=RECEIPT_REV_MISMATCH verdict=REFUSED
exit=3
```

The gate is live: a different revision is refused without `--paths`.

**G. JSON form of the copied rev** (`{"rev": "<R>", "C2_R56_PASS": true}`): `GATE OK ... revs=2f5512a8...` / `verdict=PASS` / `exit=0`. The JSON `"rev"` token is treated the same as `rev=`.

**H. No rev token**: `GATE REFUSED ... code=RECEIPT_REV_ABSENT no rev= token` / `verdict=REFUSED` / `exit=3`. Only a missing token is refused.

**J. Verdict content is not read.** `printf 'VERDICT: rev=%s C1_R56_PASS=false C2_R56_PASS=false total=6\n' "$R"` gives `GATE OK ... verdict=PASS` / `exit=0`. A failing verdict with the certified rev passes.

**K. Ancestor copy with byte-identical declared surface.** `git -C "$L" diff --name-only "$C0" "$R" -- tools/receipt-revision-gate.py | wc -l` printed `0`. With `--paths` naming that file, a receipt carrying `rev=<C0>` and `C2_R56_PASS=true` gives `GATE OK ... revs=c0137451f5b7...` / `verdict=PASS` / `exit=0`.

**L. Control for K: the same receipt with paths that drift.** `--paths` naming `tools/receipt-revision-gate.py` and `.ufo/evidence/round-21/coldread/ledger.json` gives `GATE REFUSED ... code=RECEIPT_REV_CONTENT_DRIFT drift=.ufo/evidence/round-21/coldread/ledger.json` / `verdict=REFUSED` / `exit=3`. The content check works when its paths list covers a drifting file. The `--paths` list is chosen by the caller, so an ancestor copy passes whenever the list is small enough.

**M. The gate's own selftest** (`python3 "$G" --selftest`): `GATE_SELFTEST: 19/19 pass`, exit 0. The selftest has no case for a copied rev with a fabricated verdict, so it does not cover this attack.

**N. The round's stated cannot_see** (contract.json, C2): "whether a receipt that names the certified revision was actually produced by the run it claims (a copied `rev=` token passes); the digest sidecar narrows but does not close that gap, and the report says so."

**O. Counter arm 5 is the same blind spot.** `c2/measure.py` lines 203–231 read `OWN_A`, `OWN_B`, and `OWN_PATHS` from the committed tree at `rev` (via `show(lane, rev, …)`), copy their `.sha256` siblings, and run the gate with `--paths` and `:control`/`:positive` roles. A hand-written receipt committed at `rev` with a `rev=` token that names `rev` passes arm 5 without any controls run. This is the do-nothing vulnerability the round already records; the attack above reproduces it at the gate level.

## Accuracy of the round's cannot_see sentence

- "a copied `rev=` token passes": **confirmed** (A, B, C, E, G, J).
- "the digest sidecar narrows but does not close that gap": **confirmed, and the word "narrows" overstates it.** The sidecar only detects a receipt that changed after its sidecar was written (D). Anyone who can write the receipt can write the sidecar (C). It adds no protection against a forger.
- "whether a receipt … was actually produced by the run it claims": **accurate, and the gate's scope is narrower still.** The gate cannot see:
  1. the verdict values (J: a FAIL verdict passes);
  2. whether the receipt is tracked, committed, or in a clean tree (A runs on a file in a scratch directory outside the lane);
  3. whether any control or counter produced the text (every case above is hand-written);
  4. which revision a forger chose beyond the one `rev=` token (K: an ancestor passes when `--paths` lists only identical files).
- Missing from the sentence: that the gate is a binding check (rev resolves, equals certified or matches on the listed paths, digest matches, one required line appears), not an authenticity check.

## Consequence for C2

This seat did not run the gate on the real red-before receipts (`round-54`, `round-55`); that check belongs to the deciding run and is not claimed here. The attack shows that a *passing* C2 verdict says only that the receipts bind to the certified revision by bytes and token. It does not say that a control was run. The C2 target therefore does not pass the claim-sizing do-nothing test, as the wave-2 critic also found. A measured `C2_R56_PASS=true` from the frozen counter can be recorded, but it cannot be presented as admission evidence unless the deciding run re-derives the controls itself.

## Smallest safe correction (diff only, not applied)

The gate cannot be made to authenticate receipts from bytes alone; no check on the file can distinguish a hand-written line from a counter's output. The only closing evidence is the deciding run re-executing `controls.sh` and both counters at the certified revision in a clean tree, which is what the round's deciding-run script is for. The minimal honest change is to the sentence, not the code:

```diff
 cannot_see: whether a receipt that names the certified revision was actually produced
-by the run it claims (a copied `rev=` token passes); the digest sidecar narrows but does
-not close that gap, and the report says so.
+by the run it claims. The gate checks binding only: the rev token resolves, equals the
+certified commit (or matches it on the listed --paths), the .sha256 sidecar (if present)
+matches the bytes, and a required line appears. It does not parse verdict values, check git
+tracking, or prove that any run produced the text. A receipt written by hand with the
+certified rev and a verdict line passes (copied-rev attack, reproduced at the gate); the
+sidecar detects only edits made after it was written. Admission requires the deciding run to
+re-derive the receipts.
```

This does not change the frozen counter or the target; the wording change would have to be made by L1 in the lane document that states the rule.

## Reproduction

Run from any scratch directory: `export L=/home/vgpnk/Projects/shokunin/tameshi-shokunin G=$L/tools/receipt-revision-gate.py R=2f5512a8ab0771fb2eee463ec16db359174f5edd S=$(mktemp -d)`, then the commands in A–M. Each output above was copied from the run.
