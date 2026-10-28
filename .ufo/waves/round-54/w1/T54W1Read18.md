# T54W1Read18 — cold read of `### Round-15 gate/probe registry`

- cand (C0): `59c38109bf119d0e9d4f878644a82babc937bc1e`
- span from `.ufo/waves/round-54/reader-section.py`: start 1702, end 1732
- section_sha256: `da6ef23c23f06af0c420a87476364031b107f82cf16260900040a6cb3fdac516`
- findings: 1

The section bytes were read with `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 59c38109bf119d0e9d4f878644a82babc937bc1e:SKILL.md` lines 1702-1732 (no working-tree read; the working tree carries other seats' uncommitted edits).

## F1 — the disposition selftest exit set is stale at C0 and contradicts the same sentence

Quote (byte-exact, occurs once in the section): `(the disposition selftest: 0 pass, 1 case failure or an uncaught setup traceback; round 17)`

Why: At C0 a set-but-unusable TMPDIR makes the disposition selftest exit 2 with a one-line could-not-evaluate and no traceback (`tools/evidence-disposition.py:3228-3233`; `tools/registry.json` row `evidence-disposition-selftest`), so the stated 0/1 arms are stale against the artifact the row cites and contradict the same sentence's exit-2 setup-inability arm for context-capture.

Evidence (commands run in the lane, TMPDIR pointed at my scratch):

1. Runtime arm at C0:

```
$ TMPDIR=/nonexistent-scratch-xyz python3 tools/evidence-disposition.py --selftest
exit=2
--out--   (empty)
--err--
evidence-disposition.py: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/nonexistent-scratch-xyz' (could-not-evaluate)
```

2. The tool's own exit wiring at C0 (`tools/evidence-disposition.py:3228-3233`):

```
    if options["selftest"]:
        try:
            return selftest()
        except ScratchRootUnusable as exc:
            sys.stderr.write("evidence-disposition.py: could-not-evaluate: {}\n".format(exc))
            return 2
```

with `class ScratchRootUnusable(RuntimeError): """A set-but-unusable TMPDIR: could-not-evaluate (exit 2), never a traceback."""` at lines 191-192.

3. The C0 registry row contradicts the same cell (`tools/registry.json`, row `evidence-disposition-selftest`):

```
"scratch_root": "TMPDIR set but unusable => exit 2, could-not-evaluate (the value is named, no traceback); ..."
```

4. The text was accurate before C0 and became stale because C0 changed the tool, not the page: at base `d33053f7552d`, `strict_scratch_root()` raised a plain `RuntimeError` and `main()` had no `ScratchRootUnusable` catch, so the same command at base is an uncaught traceback with exit 1:

```
$ (git archive d33053f7552d | tar -x -C $S/arch) && cd $S/arch
$ TMPDIR=/nonexistent-scratch-xyz python3 tools/evidence-disposition.py --selftest
exit=1
RuntimeError: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/nonexistent-scratch-xyz' (could-not-evaluate)
```

5. The second tool's arm in the same sentence is correct at C0 and exposes the asymmetry: `python3 tools/context-capture.py --selftest` exits 0 (`SELFTEST: PASS (49/49)`) on a usable scratch root and exits 2 with `SELFTEST: FAIL (setup error: RuntimeError: ...)` on an unusable one; `tools/context-capture.py` returns 1 only for case failure (`tools/context-capture.py:1796-1799`) and 2 for setup error (`:2215-2217`).

Proposed correction (for a fixer, not applied by this seat): make the parenthetical read `(the disposition selftest: 0 pass, 1 case failure, 2 setup inability, e.g. a set-but-unusable TMPDIR)`.

## Opened artifacts and checks — everything else in the section resolves at C0

| Check | Opened | Result |
|---|---|---|
| Row 1 entry command | `python3 tools/context-capture.py --check` in the lane | exit 0, `CONTEXT: OK (id=context_consistent receipt=.ufo/evidence/round-14/context-receipt.json sha256=05cb55b8... exit=0 findings=0)` |
| Row 1 pinned receipt digest | `git show C0:.ufo/evidence/round-14/context-receipt.json \| sha256sum` | `05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a` — matches the cell |
| Row 1 negative fixture digest | `git show C0:.ufo/evidence/round-14/context-missing-env.json \| sha256sum` | `1ee9d09bc5277fd17b90c7f21e0ed4126825c97875b32b60dfcc2ca2852aa208` — matches the cell |
| Row 1 expected-pin schema | `tools/context-capture.py:141 EXPECTED_SCHEMA = "tameshi-context-expected-v1"`, `EXPECTED_KEYS = schema/receipt_sha256/id/exit` | matches `(\`receipt_sha256\`/\`id\`/\`exit\`)` |
| Row 1 selftest command | `python3 tools/context-capture.py --selftest` | exit 0, `SELFTEST: PASS (49/49)` |
| Row 2 superseded entry | `--root . --dispositions .ufo/evidence/round-14/dispositions.json --json` | exit 2, `"kind": "expected_input_digest_mismatch"` — matches the "superseded in round 17" parenthetical |
| Row 2 live entry | `--dispositions .ufo/evidence/round-18/dispositions.json --json` | exit 0, `effective 11 / superseded 1 / findings 0` — matches "→ 0" |
| Row 2 "(round 17's now 2)" | `--dispositions .ufo/evidence/round-17/dispositions.json --json` | exit 2, `expected_input_digest_mismatch` |
| Row 2 frozen replay | `git archive 28aeef4 \| tar -x -C $S/arch`, then the round-14 command in that tree | exit 0 — matches "frozen replay: cwd = extracted `git archive 28aeef4` → 0" (commit `28aeef4` exists: "round-15 verifier spot-check (integrator, hyaku)") |
| "see the round-17 re-pin section" | `SKILL.md` at C0 lines 1840 (`## Live-tree re-pin and entry-command monitor — round 17`) and 1872 (`### Round-17 gate/probe registry — re-pin and monitor`) | anchor resolves |
| Row 2 selftest command | `python3 tools/evidence-disposition.py --selftest` | exit 0, `SELFTEST: PASS (66/66)` |
| Row 2 verdict map | `tools/evidence-disposition.py` header lines 167-181 | 0 clean / 1 failed semantic expectations / 2 and 64 could-not-evaluate declared as stated |
| "A clean result with a wrong id/exit pin becomes failed/exit1" | `tools/context-capture.py` finding table (`expected_verdict_mismatch exit 1`) | consistent |
| "Could-not-evaluate takes precedence ... stays exit2" | `tools/context-capture.py:103-105` ("Tamper, malformed and other could-not-evaluate results never become exit 1") | consistent |
| "Help exits0 only as a non-verdict informational mode" | `--help` on both tools | exit 0 each; `context-capture.py` with no arguments exits 64 (usage) |
| "the six recorded cases at this write (seven since round 16)" | `SKILL.md` at C0 line 1780 `## Seventh recorded case and full-page cold-read — round 16` | the dated six ("at this write" = round 15) plus "seven since round 16" is consistent; the later eighth/ninth case sections (lines 1931, 2130) do not contradict a dated count |
| "the Gate standard's \"Two evidences\"" | `/home/vgpnk/Projects/shokunin/PROTOCOL.md:224` and `:390` | the fleet-root protocol defines "Two evidences"; the round-15 table itself records `../PROTOCOL.md` §Gate standard |

## Examined, not filed

- `historical expected pins13 original inputs` (row 2 pinned values) is missing a space; the value checks out — `.ufo/evidence/round-13/expected.json` carries `inputs` with 13 entries — so this is cosmetic, not a stale cell.
- `and before counterpart pin historical expected/receipts` (row 2) is elliptical but asserts no checkable value; every path it names exists at C0.

No lane file was edited by this seat; the section is reported, not fixed. Scratch tree `/fast/scratch/hyaku/tameshi-r54/T54W1Read18/` was removed at the end of the seat.
