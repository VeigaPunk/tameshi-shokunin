# T56W2Read18 — cold read of `### Triggers T1–T3 and the re-pin rule`

**Verdict: `verified-record`** (findings: 0 · notes: 10).

Read revision `c0137451f5b7f22d65f748fc69f1b181f55e1378` (C0), working tree never
read for section text — every byte came from `git show c0137451f5b7f22d65f748fc69f1b181f55e1378:SKILL.md`.

## Heading and section identity

- Heading: `### Triggers T1–T3 and the re-pin rule`
- Range at C0: **SKILL.md:1100–1122** (next heading `### Six-case confidence statement (round 8, measured)` at 1123; line 1122 is blank and stripped by the frozen sectionize).
- `section_sha256`: `2350210704efcc3becfbcd40a63775ad591910039744ac6d072881b3deef7801`
- Computed with the **frozen round-18** `sectionize` (`.ufo/evidence/round-18/measure.py`), never reimplemented; the same body bytes were re-hashed independently and matched. 64 sections at C0.

```
python3 - <<'PY'
import importlib.util, subprocess, hashlib
LANE="/home/vgpnk/Projects/shokunin/tameshi-shokunin"
C="c0137451f5b7f22d65f748fc69f1b181f55e1378"
spec=importlib.util.spec_from_file_location("r18", LANE+"/.ufo/evidence/round-18/measure.py")
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
raw=subprocess.run(["git","-C",LANE,"show",C+":SKILL.md"],capture_output=True,check=True).stdout
secs=m.sectionize(raw)
t=[s for s in secs if s["heading"].startswith("### Triggers T1")][0]
print("total_sections", len(secs)); print("heading:", t["heading"])
print("start:", t["start"], "end:", t["end"]); print("section_sha256:", t["sha256"])
lines=raw.decode("utf-8","surrogateescape").split("\n")
if lines and lines[-1]=="": lines.pop()
body=lines[t["start"]-1:t["end"]-1]
while body and body[-1].strip()=="": body.pop()
print("recomputed_sha256:", hashlib.sha256("\n".join(body).encode("utf-8","surrogateescape")).hexdigest())
PY
```
```
total_sections 64
heading: ### Triggers T1–T3 and the re-pin rule
start: 1100 end: 1122
section_sha256: 2350210704efcc3becfbcd40a63775ad591910039744ac6d072881b3deef7801
recomputed_sha256: 2350210704efcc3becfbcd40a63775ad591910039744ac6d072881b3deef7801
```

## What the section tells a reader to do, and whether it holds

| Claim | Result |
|---|---|
| T1 — a case reads `stale` → re-measure at the live revision, or record the STALE cell with its reason; never an edit of the recorded table | **Holds.** Matches `corpus/knowledge/closeout-r11.md:186-188`. |
| T1 live instances: tsukuroi `084951be…` (6/10) → `bba6cdf6…`; mado `d7edaab4…` (4/10) → `90d50cdd…` → `7da4ec50…` | **Holds.** Every pin recomputed from its named revision; both kill-rates reproduced by the harness itself. |
| "(both have moved again since; re-read, never carry)" | **Holds.** Live blobs are tsukuroi `aeda2cbc…` and mado `050efc72…` — neither is any pin above. |
| T2 — round 16's RerunSweep under runner `89722ddb…` (`RerunSweep.md:19-23`) reproduced case 7 | **Holds.** The cited lines carry exactly that sha and the phrase "this re-run used the committed landing revision 89722ddb"; case 7 is `kumitate scripts/round-gate.mjs`. |
| "`0673d2e5…` is the later regression/selftest runner" | **Holds.** `runner-sha256.txt:2-5` (round-17 routed R16-EV1) says precisely that; 05a2247 (11:18) postdates c699c8c (10:49). |
| T2 — mado under `b56c6e57…` re-run once by SCR-T6, 4/10, scratch not retained; the mado note keeps it U | **Holds.** `service-optin-protocol.md:232` carries the SCR-T6 row; `mutation-case-mado-verify.md:17-23` (Incident I1) keeps the reproduction U; the scratch `/tmp/w6-scr-t6-mado-sweep` is absent and no receipt is retained in the tree. |
| "the harness itself moved four times in one day", with `4dc69ef9…`/`e3f838d4…` marked as working-tree writes | **Holds.** No commit carries those two shas; the plan's 15:27:40 / 15:28:38 readings are working-tree states. The committed chain for the day is `d8abee52` (13:01) → `597e1419` (13:57) → `b56c6e57` (15:17) → `cf41efaa` (16:06) → `75ed934d` (18:28, `VERSION` = r10-2). |
| T3 — an owner lane records a re-run at a new revision → an appended row; §1–§4 are never edited (`fleet-kill-rate-ledger.md:170-173`) | **Holds** as a rule, and history corroborates it: the ledger's §1–§4 region is byte-identical across all 9 commits that touched the file. |
| The re-pin rule — a moved pin is never re-interpreted against the new bytes (`:310` ER-3, `:318` ER-4) | **Holds.** `:310` is ER-3 trigger 3 ("A moved substrate needs a **re-pin**, never a re-interpretation of the old table"); `:318` is the ER-4 heading. |
| "`moved=0 stale=0` is a complete outcome … drift is never manufactured by re-cutting cases" | **Holds.** `closeout-r11.md:191`, `service-limits.md:86`. |
| The round-8 replay receipt (tool `cf41efaa…`, four legs; 19:14:16Z, rc 0, `fleet-kill-rate-ledger.md:281`) with `REGRESSION: PASS (cases=4 passed=4; ledger legs exact: killed-delta<=0 flips<=0)` and every leg `match=10/10 … flips=0` | **Holds.** `fleet-kill-rate-ledger.md:281` carries the tool sha, "four materialized legs", the exact PASS line, the per-leg `match=10/10 flips=0` and `2026-10-14T19:14:16Z`; corroborated at `mutation-case-kumitate-claims.md:316-317` and `reports/r7-aud-t7.md:149`. |

## The action a reader is told to run, executed

The section names no command of its own, so I took its T2 action ("re-run the reproduction under the new revision and record both pins") to be the lane's registered reproduction — `bash tools/mutate-and-run.sh --regression --workdir DIR` (`SKILL.md:2192`) — and the T1 action to be the ER-3 pin read (`fleet-kill-rate-ledger.md:289-290`).

Scratch fleet: `git clone --shared` of tameshi/kumitate/kagi/tsukuroi/mado into the seat scratch; tameshi checked out `--detach c0137451f5b7f22d65f748fc69f1b181f55e1378` (`git -C <clone> rev-parse --show-toplevel` == the clone; clone tree clean). No mutating git/jj command was run anywhere; the fleet working trees were read only.

```
bash tools/mutate-and-run.sh --regression --workdir <scratch>/regr
```
```
REGRESSION_TOOL: … sha256=977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda
REGRESSION_DATE: 2026-10-28T19:40:59Z
REGRESSION_TABLE bash-tsukuroi-census: match=10/10 recorded-killed=6 measured-killed=6 survived=4 inconclusive=0 flips=0
REGRESSION_CASE bash-tsukuroi-census: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION_TABLE bash-mado-verify: match=10/10 recorded-killed=4 measured-killed=4 survived=6 inconclusive=0 flips=0
REGRESSION_CASE bash-mado-verify: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION_CASE js-round-gate: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
… (all ten legs PASS)
REGRESSION: PASS (cases=10 passed=10; ledger legs exact: killed-delta<=0 flips<=0)
```
Exit 0, 162 s. Each leg is materialized from its sibling repo's **git object store** at the recorded revision (`REGRESSION_PIN … source=git`), so the tsukuroi and mado legs ran at `084951be…`/`d7edaab4…` while those working trees had moved on — the section's closing sentence ("the recorded tables hold at their own pinned blobs regardless of the live drift above") is therefore demonstrated, not merely asserted.

ER-3 pin read, verbatim (`sha256sum` · `git show HEAD:<path> | sha256sum` · `git status --porcelain -- <path>` · `git merge-base --is-ancestor`):

```
tsukuroi-shokunin / tools/tsukuroi-census.sh
sha256sum <gate-file>:                     aeda2cbcdcc4b08b09fefcddc237da7c0d8ee903aaf063a1578452081e0245dc
git show HEAD:<path> | sha256sum:          aeda2cbcdcc4b08b09fefcddc237da7c0d8ee903aaf063a1578452081e0245dc
git status --porcelain -- <path>:          (empty; exit 0)
git merge-base --is-ancestor 165307fe HEAD: (exit 0)
mado-shokunin / tools/mado-verify.sh
sha256sum <gate-file>:                     050efc720599345a73bdce6c1d13d50eadeee9769c2ece02462223d0156703f1
git show HEAD:<path> | sha256sum:          050efc720599345a73bdce6c1d13d50eadeee9769c2ece02462223d0156703f1
git status --porcelain -- <path>:          (empty; exit 0)
git merge-base --is-ancestor eead56b2 HEAD: (exit 0)
```
Both cases read `stale` today, exactly as T1's parenthetical says.

Pins recomputed from their named revisions:

```
git -C tameshi-shokunin show c699c8c:tools/mutate-and-run.sh | sha256sum → 89722ddb3082abd63136d025e0dfb08dcea9ffd91d58878beb230241b61f5594
git -C tameshi-shokunin show 05a2247:tools/mutate-and-run.sh | sha256sum → 0673d2e5374b94c651238e7497cbebaffb6483348400747b08f9d27cdc8118aa
git -C tsukuroi-shokunin show 165307fe:tools/tsukuroi-census.sh | sha256sum → 084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5
git -C tsukuroi-shokunin show aa136d69:tools/tsukuroi-census.sh | sha256sum → bba6cdf6f5b7a7372e43230821bb7c12aa64192266c549f39475c948803a4f55
git -C mado-shokunin show eead56b2:tools/mado-verify.sh | sha256sum → d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13
git -C mado-shokunin show 0c20a76f:tools/mado-verify.sh | sha256sum → 90d50cdd4d18410bd1e4222e12f566986c5d8d8cfdffd6f86864a3de5a3100bd
git -C mado-shokunin show 12c8f08a:tools/mado-verify.sh | sha256sum → 7da4ec5013583c91942538986b05e7243b3edeb8e3dd37b54f6b65a9225f2f4f
```

## Notes (improvements / stale-but-true; no action required for the binder)

1. **"(corrected round 18)" has no in-corpus target at C0.** `corpus/lessons/round-18.md` contains 0 occurrences of `RerunSweep`, `0673d2e5` and `89722ddb`. The round-18 correction is locatable only in git history — `git log -S 'reproduced case 7' -- SKILL.md` → `9ee1c80` ("round-18: wave-2 corrections") introduced the wording. The sibling label "(corrected round 27, seat Read15)" *does* resolve (`.ufo/waves/round-27/w1/Read15.md`, finding F1 is exactly this runner pin), so the two labels are asymmetric in traceability.
2. **Reading order invites a wrong inference.** Round 18 actually wrote the *wrong* runner (`0673d2e5…`); `89722ddb…` landed with the round-27 correction. Both facts are in the same sentence, so the text is true — but "(corrected round 18)" followed by the corrected pin can be read as dating the current pin to round 18.
3. **The T1 chains elide the owner-hardening revisions.** The ledger's readable chains are tsukuroi `084951be` → `aae45531` → `bba6cdf6` (`fleet-kill-rate-ledger.md:337`) and mado `d7edaab4` → `c4c1afb7` → `90d50cdd` → `7da4ec50` (`:338`); the section's arrows read as the complete chain but skip those two intermediates.
4. **`RerunSweep.md:93` supports the sha only.** The "r10-2" label sits at `RerunSweep.md:21` and the 18:28 time is commit 606716f's timestamp; the tool's own `VERSION` at 606716f is `mutate-and-run.sh r10-2`, so the claim stands.
5. **"rc 0" is one hop from the cited line.** `fleet-kill-rate-ledger.md:281` carries the PASS line and the 19:14:16Z stamp; the literal "rc 0" is at `mutation-case-kumitate-claims.md:316-317` (which `:281` itself names) and `reports/r7-aud-t7.md:149`.
6. **T3's pointer supports the consequence, not the trigger.** `fleet-kill-rate-ledger.md:170-173` does carry "change as an appended row, not an edit of §1–§4", but those lines describe the ledger's *own* embedding line changing rather than an owner lane recording a re-run; the rule in T3's own words is at `:312` (ER-3) and `:318` (ER-4). Round-27 seat Read15 raised the same mismatch (MG5); it survives at C0.
7. **"No recorded table was re-interpreted" is now history-backed, not just asserted.** Diffing the ledger's §1–§4 region across all 9 commits that touched `corpus/knowledge/fleet-kill-rate-ledger.md` (from its creation at 9f1d3c3 to C0) shows the region byte-identical at every commit.
8. **Pointer hygiene is fine.** `RerunSweep.md` is a unique basename in the lane tree. `service-optin-protocol.md` and `mutation-case-mado-verify.md` have two copies each, byte-identical (sha256 `84d0c154…`, `f2d53d49…`). `fleet-kill-rate-ledger.md` has three copies; the round-53 and round-18 copies differ from `corpus/knowledge/` only by blocks appended after line 422, so all four cited line numbers (`:170-173`, `:281`, `:310`, `:318`) carry the same text in all three.
9. **The T2 action is executable today.** The section names no command, but the lane's registered reproduction (`SKILL.md:2192`) runs green at C0, so a reader following T2 gets a working action rather than a dead one.
10. **Census row budget (for the L1, not a defect of this section).** `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` exits 0; the tree carries **142** SOURCES rows at C0 (base `981c5e8` had 140; C0 added S281/S282). The brief's "141 rows after this round's one new row" is one below the C0 tree.

## Commands run

Listed in full in the sibling JSON (`commands`, 18 entries). Summary: frozen round-18 `sectionize` over `git show <C0>:SKILL.md`; the C0 section text; every cited corpus/plan/wave file at its cited lines; per-revision `git show <rev>:<path> | sha256sum` for all seven cited pins; the harness `--regression` in a scratch fleet clone at C0 (exit 0, 10/10 legs exact); the ER-3 pin read on both named cases; `git log -S` for the two correction attributions; the per-commit §1–§4 immutability diff; and the sources census.

## Deliverables

- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-56/w2/T56W2Read18.json`
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-56/w2/T56W2Read18.md`
- receipts: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-56/w2/T56W2Read18-receipts/` (R1 section hash, R4 pins, R6 live pins, R7 ER-3 pin read, R8 regression, R10 pointer copies)

`SKILL.md` was not edited. No lane production file and no frozen instrument under `.ufo/evidence/round-56/` was touched. No tool was installed or upgraded.
