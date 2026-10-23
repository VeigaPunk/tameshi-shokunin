# Cold read — Read08A — SKILL.md:1609–1675 at 9f3084bc60ad56aac01e4556ef4c7653df2f65e5

Section: `## Context gate classification and explicit exit classes — round 15` (runs to line 1675; next heading `### Round-15 gate/probe registry` at 1676). Class: record. Fleet-mirror clone `/tmp/Read08A-M6sh/fleet/tameshi-shokunin`, detached at the pinned rev; whole-page sha256 verified `c46ec02e…36d6` before reading. No live-lane file opened during traces; none of the four appended files touched.

```json
{"schema": "tameshi-coldread-report-v2", "seat": "TameshiR29.Read08A", "skill_sha256": "c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6", "read_rev": "9f3084bc60ad56aac01e4556ef4c7653df2f65e5",
  "sections": [{"start": 1609, "heading": "## Context gate classification and explicit exit classes \u2014 round 15", "class": "record", "verdict": "verified-record", "blocking_gaps": [], "wrong_expectations": [],
    "minor_gaps": [],
    "commands_executed": [
      "python3 tools/trace-inputs.py --root /tmp/Read08A-M6sh/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/TameshiR29.Read08A-1.json -- python3 -c \"import sys,hashlib; [print(p, hashlib.sha256(open(p,'rb').read()).hexdigest(), len(open(p,'rb').read())) for p in sys.argv[1:]]\" .ufo/evidence/round-14/capture-context.py .ufo/evidence/round-15/verification-3.json .ufo/evidence/round-14/context-missing-env.json .ufo/evidence/round-14/context-receipt.json corpus/lessons/round-15.md corpus/lessons/round-14-verifier-spotcheck.md corpus/SOURCES.md tools/context-capture.py /home/vgpnk/Projects/shokunin/PROTOCOL.md",
      "python3 tools/trace-inputs.py --root /tmp/Read08A-M6sh/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/TameshiR29.Read08A-2.json -- python3 tools/context-capture.py --check",
      "python3 tools/trace-inputs.py --root /tmp/Read08A-M6sh/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/TameshiR29.Read08A-3.json -- python3 tools/context-capture.py --bogus-flag",
      "python3 tools/trace-inputs.py --root /tmp/Read08A-M6sh/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/TameshiR29.Read08A-4.json -- python3 tools/context-capture.py --check --receipt .ufo/evidence/round-14/context-missing-env.json --expected /tmp/Read08A-M6sh/scratch/negpin.json",
      "python3 tools/trace-inputs.py --root /tmp/Read08A-M6sh/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/TameshiR29.Read08A-5.json -- python3 tools/evidence-disposition.py --bogus-flag",
      "python3 tools/trace-inputs.py --root /tmp/Read08A-M6sh/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/TameshiR29.Read08A-6.json -- sh -c \"python3 tools/context-capture.py --selftest; python3 tools/context-capture.py --help\""
    ],
    "opened": [".ufo/evidence/round-14/capture-context.py", ".ufo/evidence/round-14/context-missing-env.json", ".ufo/evidence/round-14/context-receipt.json", ".ufo/evidence/round-15/verification-3.json", "corpus/SOURCES.md", "corpus/lessons/round-14-verifier-spotcheck.md", "corpus/lessons/round-15.md", "tools/context-capture.py", "tools/evidence-disposition.py", "tools/registry.json"],
    "inputs": {
      ".ufo/evidence/round-14/capture-context.py": "7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89",
      ".ufo/evidence/round-14/context-missing-env.json": "1ee9d09bc5277fd17b90c7f21e0ed4126825c97875b32b60dfcc2ca2852aa208",
      ".ufo/evidence/round-14/context-receipt.json": "05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a",
      ".ufo/evidence/round-15/verification-3.json": "3c419055723319f50611eb7d2fa3de46e4d4c37fb405267609eee80aecc7d8ce",
      "corpus/SOURCES.md": "804f0b4369e87fa87a45f194e8cbb315d7ea7af56957fd4c26775eddd3751dca",
      "corpus/lessons/round-14-verifier-spotcheck.md": "d267576a0d165d81b734b6c40b5b80bf61ccd9c24c8765992093afbd097cf654",
      "corpus/lessons/round-15.md": "f13a8fe16eabbf3cfc34cd2c7d9b4ee7812cb7b98eb24955dce222e9f4db52ba",
      "tools/context-capture.py": "c4a1d1658b93c94228acd0f4bee7a29f474367dd62081dace1ae298691601726",
      "tools/evidence-disposition.py": "39ee5c5effd9bbdaafda644aada0cdb008ddee1dbfee4ac6bea93fc5a1fe51c8",
      "tools/registry.json": "c1b75366f1789121e6d5a4c8f6587f7519fef3bad60569ed274df8c7a681b73c"
    },
    "external_inputs": {
      "/home/vgpnk/Projects/shokunin/PROTOCOL.md": "886e459b2aa79b8198912ad54bd57fbb025cc424d78684a02fb3d4c832d4411a",
      "/tmp/Read08A-M6sh/scratch/negpin.json": "34679289f9675f7cbecfd1c14b358bf008e2f0706917be181c5e37ceded85561"
    },
    "traces": [
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/TameshiR29.Read08A-1.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/TameshiR29.Read08A-2.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/TameshiR29.Read08A-3.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/TameshiR29.Read08A-4.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/TameshiR29.Read08A-5.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/TameshiR29.Read08A-6.json"
    ]}]}
```

## What I checked

The section is a record (classification facts with pointers; the callable entries live in the registry sub-section at 1676+, outside this bucket). Every checkable claim held:

- **Sources.** `corpus/SOURCES.md` S051 is "Retained context-receipt gate — tools/context-capture.py" (matches "maintained retained-context gate, opened this round", dated 2026-10-20) and S049 is the Python subprocess env-mapping docs (matches "explicit child invocation"); both list `corpus/lessons/round-15.md` in used-by, which has `## Gate` and `## Mistakes`. Routed defect item 5 of `round-14-verifier-spotcheck.md` says verbatim that capture-context.py's persisted-expectation `decide()` verdict behavior makes it a gate under §Gate standard and that exit64 must map to could-not-evaluate — exactly the correction this section performs. `../PROTOCOL.md` §Gate standard exists at the fleet root and its wording (gate vs probe; undeclared nonzero reads as could-not-evaluate) matches the section's use.
- **Pinned bytes.** `.ufo/evidence/round-14/capture-context.py` hashes to the archived `7313e9a2…d89`; the negative fixture to `1ee9d09b…208`; the clean receipt to `05cb55b8…c1a`. All three match the section.
- **Instrument description and line refs.** Docstring at `:2-31` states the two-document comparison excluding only top-level `observed_at`, the exact GIT_DIR environment delta, and the positive git control; `decide()` sits exactly at `:553-580` and returns `("mismatch", 1, reasons)` / `("ok", 0, [])`; `:605-643` is the main() exit mapping. Round-13 `expected.json` and `pin-manifest.json` exist. Registry rows name only the maintained gate; the archived script has no entry-point row, and both the historical registry row and recipe step 5 above carry their archive markers ("do not run", "Archived experiment, not an entry point").
- **Retained-check semantics, run not just read.** `python3 tools/context-capture.py --check` exits 0 with `id=context_consistent`, and its traced inputs are only the frozen receipt plus the tool — it never opened a recorded root path or executed retained argv. The negative fixture passed with a caller pin naming `missing_injected_environment`/exit 1 exits 1, and it flags the receipt's stored `ok`/exit-0 as `receipt_verdict_mismatch` — stored verdicts are never trusted, exactly as claimed. Usage `--bogus-flag` exits 64 `usage_error` on both active gates (context-capture traced; evidence-disposition traced). Selftest passes 49/49 (exit 0) including `stored-verdict-lie`, `duplicate-key`, and six `usage_error/64` arms, and its traced inputs contain only the tool itself — synthetic fixtures, distinct from the retained files. `--help` exits 0.
- **Evidence status.** `.ufo/evidence/round-15/verification-3.json` is the green harness (`passed=true`, 44 checks, 0 failed) while the two earlier receipts (`verification.json`, `verification-2.json`) are retained and failed — matching "the two earlier failed harness receipts remain retained history, not green evidence".

Minor gaps: none found. Tooling installs: none.

COLDREAD Read08A: verified-record
