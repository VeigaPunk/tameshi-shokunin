```json
{"schema": "tameshi-coldread-report-v2", "seat": "read31", "skill_sha256": "386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95", "read_rev": "2227d8338c02aa9a5fd7d95c1a41b76865ad7647",
  "sections": [{"start": 1806, "heading": "### Round-16 gate/probe registry", "class": "record", "verdict": "verified-record", "blocking_gaps": [], "wrong_expectations": [],
    "minor_gaps": [], "commands_executed": [
      "python3 tools/trace-inputs.py --root /tmp/read31-qcBH/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/read31-1.json -- bash tools/mutate-and-run.sh --selftest",
      "python3 tools/trace-inputs.py --root /tmp/read31-qcBH/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/read31-2.json -- python3 .ufo/evidence/round-16/measure.py --rev 2227d8338c02aa9a5fd7d95c1a41b76865ad7647",
      "python3 tools/trace-inputs.py --root /tmp/read31-qcBH/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/read31-3.json -- python3 .ufo/evidence/round-16/coldread/assemble.py --selftest",
      "python3 tools/trace-inputs.py --root /tmp/read31-qcBH/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/read31-4.json -- python3 .ufo/evidence/round-16/attribution/reattribute.py --selftest",
      "python3 tools/trace-inputs.py --root /tmp/read31-qcBH/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/read31-5.json -- bash tools/mutate-and-run.sh --regression",
      "python3 tools/trace-inputs.py --root /tmp/read31-qcBH/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/read31-6.json -- python3 .ufo/evidence/round-16/measure.py --selftest",
      "python3 tools/trace-inputs.py --root /tmp/read31-qcBH/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/read31-7.json -- bash tools/mutate-and-run.sh --regression --target /tmp/read31-qcBH/nope",
      "python3 tools/trace-inputs.py --root /tmp/read31-qcBH/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/read31-8.json -- python3 .ufo/evidence/round-16/measure.py --rev 1111111111111111111111111111111111111111"
    ],
    "opened": ["tools/mutate-and-run.sh", "tools/trace-inputs.py", ".ufo/evidence/round-16/measure.py", ".ufo/evidence/round-16/coldread/assemble.py", ".ufo/evidence/round-16/attribution/reattribute.py", ".ufo/evidence/round-15/verification-3.json"],
    "inputs": {
      "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de",
      "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4",
      ".ufo/evidence/round-16/measure.py": "03b67f58742a95e8c28ba1bffd06bd487fdc8d4c2c3130c43b487e7768c8ffbb",
      ".ufo/evidence/round-16/coldread/assemble.py": "9ee9264aabe9f474b4ecf7cfa52b4d50274ee4a6b82d06df36812a006eb0a156",
      ".ufo/evidence/round-16/attribution/reattribute.py": "eaf564e42629634e21bc2ee1aa70932a1024d721eba664f8ed892640590015c1",
      ".ufo/evidence/round-15/verification-3.json": "3c419055723319f50611eb7d2fa3de46e4d4c37fb405267609eee80aecc7d8ce"
    },
    "external_inputs": {},
    "traces": [
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/read31-1.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/read31-2.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/read31-3.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/read31-4.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/read31-5.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/read31-6.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/read31-7.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/read31-8.json"
    ]}]}
```

What I checked. The section (SKILL.md lines 1806-1813 at 2227d8338c02aa9a5fd7d95c1a41b76865ad7647) is a four-row registry table stating, for each gate/probe, its command forms and exit codes, so I read it as a record and verified it by executing every command it names, each under the trace collector in a fleet-mirror clone detached at the read rev (SKILL.md sha256 matched the given 386de44b…).

- tools/mutate-and-run.sh --selftest exited 0 ("MUTATE_SELFTEST: 97/97 pass"), matching "selftest 0 pass". --regression exited 0 with "REGRESSION: PASS (cases=9 passed=9)", every leg flips=0 and kill-rates equal to the recorded expectations (265 s, inside the 6-minute bound), matching "0 PASS". A usage probe (--regression together with --target) exited 64 with a refusal line, matching "64 usage"; the 1 FAIL and 2 SETUP exits are asserted by the passing selftest (inconclusive-run and pin-mismatch cases) rather than by a live out-of-band leg.
- .ufo/evidence/round-16/measure.py --rev 2227d83… exited 0 with a measured JSON whose "revision" is the read rev ("0 measured"); --rev 1111…1 (40 hex, absent) exited 2 with error "rev-missing", matching "2 rev/blob missing"; --selftest exited 0 (38/38).
- .ufo/evidence/round-16/coldread/assemble.py --selftest exited 0 ("SELFTEST: all checks passed"); its internal cases exercised the claimed 1 (bucket uncovered) and 2 (heading mismatch, invalid override) exits.
- .ufo/evidence/round-16/attribution/reattribute.py --selftest exited 0 ("SELFTEST: PASS (new rule 8/8; old rule fails 5/8; old-rule fidelity 14/14)"), matching "0 corrected rule passes the oracle"; it opened .ufo/evidence/round-15/verification-3.json, which is in inputs.

Receipt hygiene: all eight receipts record rev 2227d8338c02aa9a5fd7d95c1a41b76865ad7647 (equal to read_rev), zero forbidden-file opens (SCORECARD.md, LOG.md, round-21 ledger never touched), and no live-lane reads except measure.py's two, which are exclusively under the live lane's .git/ (its --repo default resolves there for git object reads; the round-17 rule permits .git/ reads). The clone working tree stayed clean, so the input hashes above are the bytes at the read rev. No sibling files were opened by hand and no tools were installed or upgraded for this seat.
COLDREAD Read31: verified-record
