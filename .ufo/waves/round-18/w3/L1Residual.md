# L1 residual verification — not independent/blind

Seventeen final sections verified by the L1 after provider cancellations. Real executed command outputs are retained under `.ufo/evidence/round-18/final/`; fresh traces bind the final section and source-file bytes. This is input-keyed evidence, not complete required-command coverage.

```json
{
  "schema": "tameshi-coldread-report-v2",
  "seat": "L1Residual",
  "skill_sha256": "1334c5128c7e53a6834c388e71a1b90a1778e72cbbed0ceccf8c1ba0423ac1e0",
  "read_rev": "a9c94c5c3a3ae857d7ee25e54fe4cf0f53fbbaa4",
  "sections": [
    {
      "start": 131,
      "heading": "## Mutation-sweep recipe \u2014 numbered steps; bounded cold-read evidence",
      "class": "instruction",
      "verdict": "gap-minor",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [
        "L1 residual verification is not a blind non-author cold read. Real command execution receipts are ancestor-pinned (921ef807/5923d89); the read revision adds only citation/receipt files and the D/N prose correction, not executable instruments. Historical per-run timestamps and deleted scratch logs remain record-only."
      ],
      "commands_executed": [
        "Pinned-source and committed actual-execution receipt audit: .ufo/evidence/round-18/coldread/traces/L1/audit-131.json"
      ],
      "opened": [
        "corpus/knowledge/mutation-case-kimi-census.md",
        "corpus/knowledge/mutation-case-kagi-census.md",
        "corpus/README.md",
        "tools/mutate-and-run.sh",
        ".ufo/evidence/round-18/sources-check/predictions.json",
        ".ufo/evidence/round-18/final/registry-branch-aligned.stdout",
        ".ufo/evidence/round-18/final/probes.stdout",
        ".ufo/evidence/round-18/final/regression.stdout",
        ".ufo/evidence/round-18/final/case8.stdout",
        ".ufo/evidence/round-18/final/case7.stdout",
        ".ufo/evidence/round-18/final/historical.stdout",
        ".ufo/evidence/round-18/final/context.stdout",
        ".ufo/evidence/round-18/final/disposition.stdout",
        ".ufo/evidence/round-18/final/before.stdout",
        ".ufo/evidence/round-18/final/repeat.stdout",
        ".ufo/evidence/round-18/final/checks.json"
      ],
      "inputs": {
        ".ufo/evidence/round-18/final/before.stdout": "e279b328de7d08631de687a0ad587943ca0a9eecba3c046adeb31b44f7a25b0d",
        ".ufo/evidence/round-18/final/case7.stdout": "e649866e5194fe54a6773582551e7fb83a33bafb0cfd661ba6b71bb8da9c7ceb",
        ".ufo/evidence/round-18/final/case8.stdout": "b4f264c375833f3c65d3ea00606851df58edc6c575617d4034f08ccfdf63694b",
        ".ufo/evidence/round-18/final/checks.json": "fed3c8e6cba05c41d8fdcafc091328e3092e2018a42fb8a8594bd8b5815c671d",
        ".ufo/evidence/round-18/final/context.stdout": "337aa6d8b19b2a82ed7de8854bf39a964076126c72bcc0b51798eca6bb134994",
        ".ufo/evidence/round-18/final/disposition.stdout": "596975d456657c8d683b6cae4382bdc958cda0084a2cd54d4b979957f55048e4",
        ".ufo/evidence/round-18/final/historical.stdout": "9050c284e68d6538ebedfc6a084fc0b4529fd50a691c72d9f7a4e570fa214590",
        ".ufo/evidence/round-18/final/probes.stdout": "d37c99e33eeb22b1b74b47b5fca26b228407792a5741bfaebc1b8be39aeb8cf0",
        ".ufo/evidence/round-18/final/registry-branch-aligned.stdout": "6502cb387613b08c64f0be73f41ff094575639f952ad1f2c4c8e76834d5517c4",
        ".ufo/evidence/round-18/final/regression.stdout": "226be3d529337dc87334b0e7c55a012fb0793865570565b84471aab6d836acfe",
        ".ufo/evidence/round-18/final/repeat.stdout": "9cd7809032b2a970bdc19577c57757e2d91e7e14f360cb37f5105eb3a0c3c21e",
        ".ufo/evidence/round-18/sources-check/predictions.json": "5749a27a92c862278a2c77307496f2b80b3c6619c6125def0ea0066b7252d35f",
        "corpus/README.md": "7fc9cb4c9ed3a49889d0a154a6351c28357dfe583027665ceeb7219150f93562",
        "corpus/knowledge/mutation-case-kagi-census.md": "0d5dc3cd7d2d21a38a65f421adb2da28685b610be4f57d1cc3572e04119815e4",
        "corpus/knowledge/mutation-case-kimi-census.md": "034524eff8f19cb8fca78cd5d13c6da9971f2ef2b5bedc1b950309c95c121548",
        "tools/mutate-and-run.sh": "d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b"
      },
      "external_inputs": {},
      "traces": [
        ".ufo/evidence/round-18/coldread/traces/L1/audit-131.json"
      ]
    },
    {
      "start": 921,
      "heading": "## The leg ledger \u2014 replay, receipt, and how it is read (round 7, measured)",
      "class": "record",
      "verdict": "gap-minor",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [
        "L1 residual verification is not a blind non-author cold read. Real command execution receipts are ancestor-pinned (921ef807/5923d89); the read revision adds only citation/receipt files and the D/N prose correction, not executable instruments. Historical per-run timestamps and deleted scratch logs remain record-only."
      ],
      "commands_executed": [
        "Pinned-source and committed actual-execution receipt audit: .ufo/evidence/round-18/coldread/traces/L1/audit-921.json"
      ],
      "opened": [
        "corpus/knowledge/fleet-kill-rate-ledger.md",
        "tools/mutate-and-run.sh",
        ".ufo/evidence/round-18/final/registry-branch-aligned.stdout",
        ".ufo/evidence/round-18/final/probes.stdout",
        ".ufo/evidence/round-18/final/regression.stdout",
        ".ufo/evidence/round-18/final/case8.stdout",
        ".ufo/evidence/round-18/final/case7.stdout",
        ".ufo/evidence/round-18/final/historical.stdout",
        ".ufo/evidence/round-18/final/context.stdout",
        ".ufo/evidence/round-18/final/disposition.stdout",
        ".ufo/evidence/round-18/final/before.stdout",
        ".ufo/evidence/round-18/final/repeat.stdout",
        ".ufo/evidence/round-18/final/checks.json"
      ],
      "inputs": {
        ".ufo/evidence/round-18/final/before.stdout": "e279b328de7d08631de687a0ad587943ca0a9eecba3c046adeb31b44f7a25b0d",
        ".ufo/evidence/round-18/final/case7.stdout": "e649866e5194fe54a6773582551e7fb83a33bafb0cfd661ba6b71bb8da9c7ceb",
        ".ufo/evidence/round-18/final/case8.stdout": "b4f264c375833f3c65d3ea00606851df58edc6c575617d4034f08ccfdf63694b",
        ".ufo/evidence/round-18/final/checks.json": "fed3c8e6cba05c41d8fdcafc091328e3092e2018a42fb8a8594bd8b5815c671d",
        ".ufo/evidence/round-18/final/context.stdout": "337aa6d8b19b2a82ed7de8854bf39a964076126c72bcc0b51798eca6bb134994",
        ".ufo/evidence/round-18/final/disposition.stdout": "596975d456657c8d683b6cae4382bdc958cda0084a2cd54d4b979957f55048e4",
        ".ufo/evidence/round-18/final/historical.stdout": "9050c284e68d6538ebedfc6a084fc0b4529fd50a691c72d9f7a4e570fa214590",
        ".ufo/evidence/round-18/final/probes.stdout": "d37c99e33eeb22b1b74b47b5fca26b228407792a5741bfaebc1b8be39aeb8cf0",
        ".ufo/evidence/round-18/final/registry-branch-aligned.stdout": "6502cb387613b08c64f0be73f41ff094575639f952ad1f2c4c8e76834d5517c4",
        ".ufo/evidence/round-18/final/regression.stdout": "226be3d529337dc87334b0e7c55a012fb0793865570565b84471aab6d836acfe",
        ".ufo/evidence/round-18/final/repeat.stdout": "9cd7809032b2a970bdc19577c57757e2d91e7e14f360cb37f5105eb3a0c3c21e",
        "corpus/knowledge/fleet-kill-rate-ledger.md": "13a11e468dbf26972bb9734c2f0bedec859386f6729225c367c61ba056d7499e",
        "tools/mutate-and-run.sh": "d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b"
      },
      "external_inputs": {},
      "traces": [
        ".ufo/evidence/round-18/coldread/traces/L1/audit-921.json"
      ]
    },
    {
      "start": 965,
      "heading": "### Reading a receipt \u2014 the discipline",
      "class": "instruction",
      "verdict": "gap-minor",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [
        "L1 residual verification is not a blind non-author cold read. Real command execution receipts are ancestor-pinned (921ef807/5923d89); the read revision adds only citation/receipt files and the D/N prose correction, not executable instruments. Historical per-run timestamps and deleted scratch logs remain record-only."
      ],
      "commands_executed": [
        "Pinned-source and committed actual-execution receipt audit: .ufo/evidence/round-18/coldread/traces/L1/audit-965.json"
      ],
      "opened": [
        "corpus/knowledge/fleet-kill-rate-ledger.md",
        "tools/mutate-and-run.sh",
        ".ufo/evidence/round-18/final/registry-branch-aligned.stdout",
        ".ufo/evidence/round-18/final/probes.stdout",
        ".ufo/evidence/round-18/final/regression.stdout",
        ".ufo/evidence/round-18/final/case8.stdout",
        ".ufo/evidence/round-18/final/case7.stdout",
        ".ufo/evidence/round-18/final/historical.stdout",
        ".ufo/evidence/round-18/final/context.stdout",
        ".ufo/evidence/round-18/final/disposition.stdout",
        ".ufo/evidence/round-18/final/before.stdout",
        ".ufo/evidence/round-18/final/repeat.stdout",
        ".ufo/evidence/round-18/final/checks.json"
      ],
      "inputs": {
        ".ufo/evidence/round-18/final/before.stdout": "e279b328de7d08631de687a0ad587943ca0a9eecba3c046adeb31b44f7a25b0d",
        ".ufo/evidence/round-18/final/case7.stdout": "e649866e5194fe54a6773582551e7fb83a33bafb0cfd661ba6b71bb8da9c7ceb",
        ".ufo/evidence/round-18/final/case8.stdout": "b4f264c375833f3c65d3ea00606851df58edc6c575617d4034f08ccfdf63694b",
        ".ufo/evidence/round-18/final/checks.json": "fed3c8e6cba05c41d8fdcafc091328e3092e2018a42fb8a8594bd8b5815c671d",
        ".ufo/evidence/round-18/final/context.stdout": "337aa6d8b19b2a82ed7de8854bf39a964076126c72bcc0b51798eca6bb134994",
        ".ufo/evidence/round-18/final/disposition.stdout": "596975d456657c8d683b6cae4382bdc958cda0084a2cd54d4b979957f55048e4",
        ".ufo/evidence/round-18/final/historical.stdout": "9050c284e68d6538ebedfc6a084fc0b4529fd50a691c72d9f7a4e570fa214590",
        ".ufo/evidence/round-18/final/probes.stdout": "d37c99e33eeb22b1b74b47b5fca26b228407792a5741bfaebc1b8be39aeb8cf0",
        ".ufo/evidence/round-18/final/registry-branch-aligned.stdout": "6502cb387613b08c64f0be73f41ff094575639f952ad1f2c4c8e76834d5517c4",
        ".ufo/evidence/round-18/final/regression.stdout": "226be3d529337dc87334b0e7c55a012fb0793865570565b84471aab6d836acfe",
        ".ufo/evidence/round-18/final/repeat.stdout": "9cd7809032b2a970bdc19577c57757e2d91e7e14f360cb37f5105eb3a0c3c21e",
        "corpus/knowledge/fleet-kill-rate-ledger.md": "13a11e468dbf26972bb9734c2f0bedec859386f6729225c367c61ba056d7499e",
        "tools/mutate-and-run.sh": "d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b"
      },
      "external_inputs": {},
      "traces": [
        ".ufo/evidence/round-18/coldread/traces/L1/audit-965.json"
      ]
    },
    {
      "start": 1021,
      "heading": "### The tick and the pin read",
      "class": "instruction",
      "verdict": "gap-minor",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [
        "L1 residual verification is not a blind non-author cold read. Real command execution receipts are ancestor-pinned (921ef807/5923d89); the read revision adds only citation/receipt files and the D/N prose correction, not executable instruments. Historical per-run timestamps and deleted scratch logs remain record-only."
      ],
      "commands_executed": [
        "Pinned-source and committed actual-execution receipt audit: .ufo/evidence/round-18/coldread/traces/L1/audit-1021.json"
      ],
      "opened": [
        "tools/pin-disposition.py",
        "tools/mutate-and-run.sh",
        "corpus/knowledge/fleet-kill-rate-ledger.md",
        ".ufo/evidence/round-13/pin-manifest.json",
        ".ufo/evidence/round-18/final/registry-branch-aligned.stdout",
        ".ufo/evidence/round-18/final/probes.stdout",
        ".ufo/evidence/round-18/final/regression.stdout",
        ".ufo/evidence/round-18/final/case8.stdout",
        ".ufo/evidence/round-18/final/case7.stdout",
        ".ufo/evidence/round-18/final/historical.stdout",
        ".ufo/evidence/round-18/final/context.stdout",
        ".ufo/evidence/round-18/final/disposition.stdout",
        ".ufo/evidence/round-18/final/before.stdout",
        ".ufo/evidence/round-18/final/repeat.stdout",
        ".ufo/evidence/round-18/final/checks.json"
      ],
      "inputs": {
        ".ufo/evidence/round-13/pin-manifest.json": "64eaa43e3f7a928472efa32c7230ca78358235716db04947a93edb0202920af6",
        ".ufo/evidence/round-18/final/before.stdout": "e279b328de7d08631de687a0ad587943ca0a9eecba3c046adeb31b44f7a25b0d",
        ".ufo/evidence/round-18/final/case7.stdout": "e649866e5194fe54a6773582551e7fb83a33bafb0cfd661ba6b71bb8da9c7ceb",
        ".ufo/evidence/round-18/final/case8.stdout": "b4f264c375833f3c65d3ea00606851df58edc6c575617d4034f08ccfdf63694b",
        ".ufo/evidence/round-18/final/checks.json": "fed3c8e6cba05c41d8fdcafc091328e3092e2018a42fb8a8594bd8b5815c671d",
        ".ufo/evidence/round-18/final/context.stdout": "337aa6d8b19b2a82ed7de8854bf39a964076126c72bcc0b51798eca6bb134994",
        ".ufo/evidence/round-18/final/disposition.stdout": "596975d456657c8d683b6cae4382bdc958cda0084a2cd54d4b979957f55048e4",
        ".ufo/evidence/round-18/final/historical.stdout": "9050c284e68d6538ebedfc6a084fc0b4529fd50a691c72d9f7a4e570fa214590",
        ".ufo/evidence/round-18/final/probes.stdout": "d37c99e33eeb22b1b74b47b5fca26b228407792a5741bfaebc1b8be39aeb8cf0",
        ".ufo/evidence/round-18/final/registry-branch-aligned.stdout": "6502cb387613b08c64f0be73f41ff094575639f952ad1f2c4c8e76834d5517c4",
        ".ufo/evidence/round-18/final/regression.stdout": "226be3d529337dc87334b0e7c55a012fb0793865570565b84471aab6d836acfe",
        ".ufo/evidence/round-18/final/repeat.stdout": "9cd7809032b2a970bdc19577c57757e2d91e7e14f360cb37f5105eb3a0c3c21e",
        "corpus/knowledge/fleet-kill-rate-ledger.md": "13a11e468dbf26972bb9734c2f0bedec859386f6729225c367c61ba056d7499e",
        "tools/mutate-and-run.sh": "d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b",
        "tools/pin-disposition.py": "331529eadafe9138c88c1fe09666c9401d28c166f16bc92ecc092fc4d92c3a4c"
      },
      "external_inputs": {},
      "traces": [
        ".ufo/evidence/round-18/coldread/traces/L1/audit-1021.json"
      ]
    },
    {
      "start": 1164,
      "heading": "### The tick, executed",
      "class": "record",
      "verdict": "gap-minor",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [
        "L1 residual verification is not a blind non-author cold read. Real command execution receipts are ancestor-pinned (921ef807/5923d89); the read revision adds only citation/receipt files and the D/N prose correction, not executable instruments. Historical per-run timestamps and deleted scratch logs remain record-only."
      ],
      "commands_executed": [
        "Pinned-source and committed actual-execution receipt audit: .ufo/evidence/round-18/coldread/traces/L1/audit-1164.json"
      ],
      "opened": [
        "corpus/knowledge/fleet-kill-rate-ledger.md",
        "tools/mutate-and-run.sh",
        ".ufo/evidence/round-18/final/registry-branch-aligned.stdout",
        ".ufo/evidence/round-18/final/probes.stdout",
        ".ufo/evidence/round-18/final/regression.stdout",
        ".ufo/evidence/round-18/final/case8.stdout",
        ".ufo/evidence/round-18/final/case7.stdout",
        ".ufo/evidence/round-18/final/historical.stdout",
        ".ufo/evidence/round-18/final/context.stdout",
        ".ufo/evidence/round-18/final/disposition.stdout",
        ".ufo/evidence/round-18/final/before.stdout",
        ".ufo/evidence/round-18/final/repeat.stdout",
        ".ufo/evidence/round-18/final/checks.json"
      ],
      "inputs": {
        ".ufo/evidence/round-18/final/before.stdout": "e279b328de7d08631de687a0ad587943ca0a9eecba3c046adeb31b44f7a25b0d",
        ".ufo/evidence/round-18/final/case7.stdout": "e649866e5194fe54a6773582551e7fb83a33bafb0cfd661ba6b71bb8da9c7ceb",
        ".ufo/evidence/round-18/final/case8.stdout": "b4f264c375833f3c65d3ea00606851df58edc6c575617d4034f08ccfdf63694b",
        ".ufo/evidence/round-18/final/checks.json": "fed3c8e6cba05c41d8fdcafc091328e3092e2018a42fb8a8594bd8b5815c671d",
        ".ufo/evidence/round-18/final/context.stdout": "337aa6d8b19b2a82ed7de8854bf39a964076126c72bcc0b51798eca6bb134994",
        ".ufo/evidence/round-18/final/disposition.stdout": "596975d456657c8d683b6cae4382bdc958cda0084a2cd54d4b979957f55048e4",
        ".ufo/evidence/round-18/final/historical.stdout": "9050c284e68d6538ebedfc6a084fc0b4529fd50a691c72d9f7a4e570fa214590",
        ".ufo/evidence/round-18/final/probes.stdout": "d37c99e33eeb22b1b74b47b5fca26b228407792a5741bfaebc1b8be39aeb8cf0",
        ".ufo/evidence/round-18/final/registry-branch-aligned.stdout": "6502cb387613b08c64f0be73f41ff094575639f952ad1f2c4c8e76834d5517c4",
        ".ufo/evidence/round-18/final/regression.stdout": "226be3d529337dc87334b0e7c55a012fb0793865570565b84471aab6d836acfe",
        ".ufo/evidence/round-18/final/repeat.stdout": "9cd7809032b2a970bdc19577c57757e2d91e7e14f360cb37f5105eb3a0c3c21e",
        "corpus/knowledge/fleet-kill-rate-ledger.md": "13a11e468dbf26972bb9734c2f0bedec859386f6729225c367c61ba056d7499e",
        "tools/mutate-and-run.sh": "d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b"
      },
      "external_inputs": {},
      "traces": [
        ".ufo/evidence/round-18/coldread/traces/L1/audit-1164.json"
      ]
    },
    {
      "start": 1212,
      "heading": "### The receipt at this boundary",
      "class": "record",
      "verdict": "gap-minor",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [
        "L1 residual verification is not a blind non-author cold read. Real command execution receipts are ancestor-pinned (921ef807/5923d89); the read revision adds only citation/receipt files and the D/N prose correction, not executable instruments. Historical per-run timestamps and deleted scratch logs remain record-only."
      ],
      "commands_executed": [
        "Pinned-source and committed actual-execution receipt audit: .ufo/evidence/round-18/coldread/traces/L1/audit-1212.json"
      ],
      "opened": [
        "corpus/knowledge/fleet-kill-rate-ledger.md",
        "tools/mutate-and-run.sh",
        ".ufo/evidence/round-18/final/registry-branch-aligned.stdout",
        ".ufo/evidence/round-18/final/probes.stdout",
        ".ufo/evidence/round-18/final/regression.stdout",
        ".ufo/evidence/round-18/final/case8.stdout",
        ".ufo/evidence/round-18/final/case7.stdout",
        ".ufo/evidence/round-18/final/historical.stdout",
        ".ufo/evidence/round-18/final/context.stdout",
        ".ufo/evidence/round-18/final/disposition.stdout",
        ".ufo/evidence/round-18/final/before.stdout",
        ".ufo/evidence/round-18/final/repeat.stdout",
        ".ufo/evidence/round-18/final/checks.json"
      ],
      "inputs": {
        ".ufo/evidence/round-18/final/before.stdout": "e279b328de7d08631de687a0ad587943ca0a9eecba3c046adeb31b44f7a25b0d",
        ".ufo/evidence/round-18/final/case7.stdout": "e649866e5194fe54a6773582551e7fb83a33bafb0cfd661ba6b71bb8da9c7ceb",
        ".ufo/evidence/round-18/final/case8.stdout": "b4f264c375833f3c65d3ea00606851df58edc6c575617d4034f08ccfdf63694b",
        ".ufo/evidence/round-18/final/checks.json": "fed3c8e6cba05c41d8fdcafc091328e3092e2018a42fb8a8594bd8b5815c671d",
        ".ufo/evidence/round-18/final/context.stdout": "337aa6d8b19b2a82ed7de8854bf39a964076126c72bcc0b51798eca6bb134994",
        ".ufo/evidence/round-18/final/disposition.stdout": "596975d456657c8d683b6cae4382bdc958cda0084a2cd54d4b979957f55048e4",
        ".ufo/evidence/round-18/final/historical.stdout": "9050c284e68d6538ebedfc6a084fc0b4529fd50a691c72d9f7a4e570fa214590",
        ".ufo/evidence/round-18/final/probes.stdout": "d37c99e33eeb22b1b74b47b5fca26b228407792a5741bfaebc1b8be39aeb8cf0",
        ".ufo/evidence/round-18/final/registry-branch-aligned.stdout": "6502cb387613b08c64f0be73f41ff094575639f952ad1f2c4c8e76834d5517c4",
        ".ufo/evidence/round-18/final/regression.stdout": "226be3d529337dc87334b0e7c55a012fb0793865570565b84471aab6d836acfe",
        ".ufo/evidence/round-18/final/repeat.stdout": "9cd7809032b2a970bdc19577c57757e2d91e7e14f360cb37f5105eb3a0c3c21e",
        "corpus/knowledge/fleet-kill-rate-ledger.md": "13a11e468dbf26972bb9734c2f0bedec859386f6729225c367c61ba056d7499e",
        "tools/mutate-and-run.sh": "d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b"
      },
      "external_inputs": {},
      "traces": [
        ".ufo/evidence/round-18/coldread/traces/L1/audit-1212.json"
      ]
    },
    {
      "start": 1436,
      "heading": "### Where to enter \u2014 four readers",
      "class": "instruction",
      "verdict": "gap-minor",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [
        "L1 residual verification is not a blind non-author cold read. Real command execution receipts are ancestor-pinned (921ef807/5923d89); the read revision adds only citation/receipt files and the D/N prose correction, not executable instruments. Historical per-run timestamps and deleted scratch logs remain record-only."
      ],
      "commands_executed": [
        "Pinned-source and committed actual-execution receipt audit: .ufo/evidence/round-18/coldread/traces/L1/audit-1436.json"
      ],
      "opened": [
        "corpus/knowledge/operator-runbook.md",
        "corpus/knowledge/closeout-r11.md",
        "corpus/knowledge/service-standing-state.md",
        "corpus/knowledge/service-optin-protocol.md",
        "corpus/knowledge/fleet-kill-rate-ledger.md",
        ".ufo/evidence/round-18/final/registry-branch-aligned.stdout",
        ".ufo/evidence/round-18/final/probes.stdout",
        ".ufo/evidence/round-18/final/regression.stdout",
        ".ufo/evidence/round-18/final/case8.stdout",
        ".ufo/evidence/round-18/final/case7.stdout",
        ".ufo/evidence/round-18/final/historical.stdout",
        ".ufo/evidence/round-18/final/context.stdout",
        ".ufo/evidence/round-18/final/disposition.stdout",
        ".ufo/evidence/round-18/final/before.stdout",
        ".ufo/evidence/round-18/final/repeat.stdout",
        ".ufo/evidence/round-18/final/checks.json"
      ],
      "inputs": {
        ".ufo/evidence/round-18/final/before.stdout": "e279b328de7d08631de687a0ad587943ca0a9eecba3c046adeb31b44f7a25b0d",
        ".ufo/evidence/round-18/final/case7.stdout": "e649866e5194fe54a6773582551e7fb83a33bafb0cfd661ba6b71bb8da9c7ceb",
        ".ufo/evidence/round-18/final/case8.stdout": "b4f264c375833f3c65d3ea00606851df58edc6c575617d4034f08ccfdf63694b",
        ".ufo/evidence/round-18/final/checks.json": "fed3c8e6cba05c41d8fdcafc091328e3092e2018a42fb8a8594bd8b5815c671d",
        ".ufo/evidence/round-18/final/context.stdout": "337aa6d8b19b2a82ed7de8854bf39a964076126c72bcc0b51798eca6bb134994",
        ".ufo/evidence/round-18/final/disposition.stdout": "596975d456657c8d683b6cae4382bdc958cda0084a2cd54d4b979957f55048e4",
        ".ufo/evidence/round-18/final/historical.stdout": "9050c284e68d6538ebedfc6a084fc0b4529fd50a691c72d9f7a4e570fa214590",
        ".ufo/evidence/round-18/final/probes.stdout": "d37c99e33eeb22b1b74b47b5fca26b228407792a5741bfaebc1b8be39aeb8cf0",
        ".ufo/evidence/round-18/final/registry-branch-aligned.stdout": "6502cb387613b08c64f0be73f41ff094575639f952ad1f2c4c8e76834d5517c4",
        ".ufo/evidence/round-18/final/regression.stdout": "226be3d529337dc87334b0e7c55a012fb0793865570565b84471aab6d836acfe",
        ".ufo/evidence/round-18/final/repeat.stdout": "9cd7809032b2a970bdc19577c57757e2d91e7e14f360cb37f5105eb3a0c3c21e",
        "corpus/knowledge/closeout-r11.md": "cea3352aa60eb51b51e2722fdb820cac19cd1514670df931212904e826940265",
        "corpus/knowledge/fleet-kill-rate-ledger.md": "13a11e468dbf26972bb9734c2f0bedec859386f6729225c367c61ba056d7499e",
        "corpus/knowledge/operator-runbook.md": "8b2e185ff011f6cfc2aee187ff1c2a1f8120e410c00f4b67eb6c7f1ebabb6859",
        "corpus/knowledge/service-optin-protocol.md": "84d0c1547eed257d921b832468d6f010bcca331e8ce67ed378852d7993da8e0e",
        "corpus/knowledge/service-standing-state.md": "d326c1a4d61c97051db07c55fb6de69bdc4faa9bbef21186d0dc0451efafb952"
      },
      "external_inputs": {},
      "traces": [
        ".ufo/evidence/round-18/coldread/traces/L1/audit-1436.json"
      ]
    },
    {
      "start": 1479,
      "heading": "## Repeated controls and gate registry \u2014 round 12",
      "class": "instruction",
      "verdict": "gap-minor",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [
        "L1 residual verification is not a blind non-author cold read. Real command execution receipts are ancestor-pinned (921ef807/5923d89); the read revision adds only citation/receipt files and the D/N prose correction, not executable instruments. Historical per-run timestamps and deleted scratch logs remain record-only."
      ],
      "commands_executed": [
        "Pinned-source and committed actual-execution receipt audit: .ufo/evidence/round-18/coldread/traces/L1/audit-1479.json"
      ],
      "opened": [
        "corpus/knowledge/repeated-control-precondition.md",
        "corpus/SOURCES.md",
        "tools/repeat-control.py",
        ".ufo/evidence/round-12/verification-final.json",
        ".ufo/evidence/round-18/final/registry-branch-aligned.stdout",
        ".ufo/evidence/round-18/final/probes.stdout",
        ".ufo/evidence/round-18/final/regression.stdout",
        ".ufo/evidence/round-18/final/case8.stdout",
        ".ufo/evidence/round-18/final/case7.stdout",
        ".ufo/evidence/round-18/final/historical.stdout",
        ".ufo/evidence/round-18/final/context.stdout",
        ".ufo/evidence/round-18/final/disposition.stdout",
        ".ufo/evidence/round-18/final/before.stdout",
        ".ufo/evidence/round-18/final/repeat.stdout",
        ".ufo/evidence/round-18/final/checks.json"
      ],
      "inputs": {
        ".ufo/evidence/round-12/verification-final.json": "9f3d117af3b613d0a00b7d0a623d31136e36f53cb6fcb5626e42cf0c6e022201",
        ".ufo/evidence/round-18/final/before.stdout": "e279b328de7d08631de687a0ad587943ca0a9eecba3c046adeb31b44f7a25b0d",
        ".ufo/evidence/round-18/final/case7.stdout": "e649866e5194fe54a6773582551e7fb83a33bafb0cfd661ba6b71bb8da9c7ceb",
        ".ufo/evidence/round-18/final/case8.stdout": "b4f264c375833f3c65d3ea00606851df58edc6c575617d4034f08ccfdf63694b",
        ".ufo/evidence/round-18/final/checks.json": "fed3c8e6cba05c41d8fdcafc091328e3092e2018a42fb8a8594bd8b5815c671d",
        ".ufo/evidence/round-18/final/context.stdout": "337aa6d8b19b2a82ed7de8854bf39a964076126c72bcc0b51798eca6bb134994",
        ".ufo/evidence/round-18/final/disposition.stdout": "596975d456657c8d683b6cae4382bdc958cda0084a2cd54d4b979957f55048e4",
        ".ufo/evidence/round-18/final/historical.stdout": "9050c284e68d6538ebedfc6a084fc0b4529fd50a691c72d9f7a4e570fa214590",
        ".ufo/evidence/round-18/final/probes.stdout": "d37c99e33eeb22b1b74b47b5fca26b228407792a5741bfaebc1b8be39aeb8cf0",
        ".ufo/evidence/round-18/final/registry-branch-aligned.stdout": "6502cb387613b08c64f0be73f41ff094575639f952ad1f2c4c8e76834d5517c4",
        ".ufo/evidence/round-18/final/regression.stdout": "226be3d529337dc87334b0e7c55a012fb0793865570565b84471aab6d836acfe",
        ".ufo/evidence/round-18/final/repeat.stdout": "9cd7809032b2a970bdc19577c57757e2d91e7e14f360cb37f5105eb3a0c3c21e",
        "corpus/SOURCES.md": "018ee9a86500efc6d07ea141d20c7de6b2ec76e5e808ffbf12508ada46a84e0e",
        "corpus/knowledge/repeated-control-precondition.md": "1339460070d6c2c2d9609915a675b6866f0c42089a39bdb1ecb39b52f1c5fe5b",
        "tools/repeat-control.py": "296fe566dc59380b6baa518b61cef92fe3c7af09d538b2dde9e7f4af1b8cbc25"
      },
      "external_inputs": {},
      "traces": [
        ".ufo/evidence/round-18/coldread/traces/L1/audit-1479.json"
      ]
    },
    {
      "start": 1676,
      "heading": "### Round-15 gate/probe registry",
      "class": "instruction",
      "verdict": "gap-minor",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [
        "L1 residual verification is not a blind non-author cold read. Real command execution receipts are ancestor-pinned (921ef807/5923d89); the read revision adds only citation/receipt files and the D/N prose correction, not executable instruments. Historical per-run timestamps and deleted scratch logs remain record-only."
      ],
      "commands_executed": [
        "Pinned-source and committed actual-execution receipt audit: .ufo/evidence/round-18/coldread/traces/L1/audit-1676.json"
      ],
      "opened": [
        "tools/context-capture.py",
        "tools/evidence-disposition.py",
        ".ufo/evidence/round-18/dispositions.json",
        ".ufo/evidence/round-14/context-receipt.json",
        ".ufo/evidence/round-18/final/registry-branch-aligned.stdout",
        ".ufo/evidence/round-18/final/probes.stdout",
        ".ufo/evidence/round-18/final/regression.stdout",
        ".ufo/evidence/round-18/final/case8.stdout",
        ".ufo/evidence/round-18/final/case7.stdout",
        ".ufo/evidence/round-18/final/historical.stdout",
        ".ufo/evidence/round-18/final/context.stdout",
        ".ufo/evidence/round-18/final/disposition.stdout",
        ".ufo/evidence/round-18/final/before.stdout",
        ".ufo/evidence/round-18/final/repeat.stdout",
        ".ufo/evidence/round-18/final/checks.json"
      ],
      "inputs": {
        ".ufo/evidence/round-14/context-receipt.json": "05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a",
        ".ufo/evidence/round-18/dispositions.json": "9caa2f76dcc36265bb11b58baa397b1015a91b086db63d203ab16020a1fc2676",
        ".ufo/evidence/round-18/final/before.stdout": "e279b328de7d08631de687a0ad587943ca0a9eecba3c046adeb31b44f7a25b0d",
        ".ufo/evidence/round-18/final/case7.stdout": "e649866e5194fe54a6773582551e7fb83a33bafb0cfd661ba6b71bb8da9c7ceb",
        ".ufo/evidence/round-18/final/case8.stdout": "b4f264c375833f3c65d3ea00606851df58edc6c575617d4034f08ccfdf63694b",
        ".ufo/evidence/round-18/final/checks.json": "fed3c8e6cba05c41d8fdcafc091328e3092e2018a42fb8a8594bd8b5815c671d",
        ".ufo/evidence/round-18/final/context.stdout": "337aa6d8b19b2a82ed7de8854bf39a964076126c72bcc0b51798eca6bb134994",
        ".ufo/evidence/round-18/final/disposition.stdout": "596975d456657c8d683b6cae4382bdc958cda0084a2cd54d4b979957f55048e4",
        ".ufo/evidence/round-18/final/historical.stdout": "9050c284e68d6538ebedfc6a084fc0b4529fd50a691c72d9f7a4e570fa214590",
        ".ufo/evidence/round-18/final/probes.stdout": "d37c99e33eeb22b1b74b47b5fca26b228407792a5741bfaebc1b8be39aeb8cf0",
        ".ufo/evidence/round-18/final/registry-branch-aligned.stdout": "6502cb387613b08c64f0be73f41ff094575639f952ad1f2c4c8e76834d5517c4",
        ".ufo/evidence/round-18/final/regression.stdout": "226be3d529337dc87334b0e7c55a012fb0793865570565b84471aab6d836acfe",
        ".ufo/evidence/round-18/final/repeat.stdout": "9cd7809032b2a970bdc19577c57757e2d91e7e14f360cb37f5105eb3a0c3c21e",
        "tools/context-capture.py": "c4a1d1658b93c94228acd0f4bee7a29f474367dd62081dace1ae298691601726",
        "tools/evidence-disposition.py": "66655a3a692b587fd0a6dc3f2cf0edd766a824eb86280753d0bd57efeecc1f44"
      },
      "external_inputs": {},
      "traces": [
        ".ufo/evidence/round-18/coldread/traces/L1/audit-1676.json"
      ]
    },
    {
      "start": 1707,
      "heading": "## Errata \u2014 round 16 full-page cold-read",
      "class": "record",
      "verdict": "gap-minor",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [
        "L1 residual verification is not a blind non-author cold read. Real command execution receipts are ancestor-pinned (921ef807/5923d89); the read revision adds only citation/receipt files and the D/N prose correction, not executable instruments. Historical per-run timestamps and deleted scratch logs remain record-only."
      ],
      "commands_executed": [
        "Pinned-source and committed actual-execution receipt audit: .ufo/evidence/round-18/coldread/traces/L1/audit-1707.json"
      ],
      "opened": [
        ".ufo/evidence/round-16/coldread/SKILL.snapshot.md",
        ".ufo/evidence/round-16/coldread/ledger.json",
        ".ufo/evidence/round-18/final/registry-branch-aligned.stdout",
        ".ufo/evidence/round-18/final/probes.stdout",
        ".ufo/evidence/round-18/final/regression.stdout",
        ".ufo/evidence/round-18/final/case8.stdout",
        ".ufo/evidence/round-18/final/case7.stdout",
        ".ufo/evidence/round-18/final/historical.stdout",
        ".ufo/evidence/round-18/final/context.stdout",
        ".ufo/evidence/round-18/final/disposition.stdout",
        ".ufo/evidence/round-18/final/before.stdout",
        ".ufo/evidence/round-18/final/repeat.stdout",
        ".ufo/evidence/round-18/final/checks.json"
      ],
      "inputs": {
        ".ufo/evidence/round-16/coldread/SKILL.snapshot.md": "97cf436b669ea445abe36cf6757202eec1c2a4bad2814b07f4159bb9dc623580",
        ".ufo/evidence/round-16/coldread/ledger.json": "b84151a35f0cefa0716f3dd200a183dee5badc7be09ba1bac11d61283f70623c",
        ".ufo/evidence/round-18/final/before.stdout": "e279b328de7d08631de687a0ad587943ca0a9eecba3c046adeb31b44f7a25b0d",
        ".ufo/evidence/round-18/final/case7.stdout": "e649866e5194fe54a6773582551e7fb83a33bafb0cfd661ba6b71bb8da9c7ceb",
        ".ufo/evidence/round-18/final/case8.stdout": "b4f264c375833f3c65d3ea00606851df58edc6c575617d4034f08ccfdf63694b",
        ".ufo/evidence/round-18/final/checks.json": "fed3c8e6cba05c41d8fdcafc091328e3092e2018a42fb8a8594bd8b5815c671d",
        ".ufo/evidence/round-18/final/context.stdout": "337aa6d8b19b2a82ed7de8854bf39a964076126c72bcc0b51798eca6bb134994",
        ".ufo/evidence/round-18/final/disposition.stdout": "596975d456657c8d683b6cae4382bdc958cda0084a2cd54d4b979957f55048e4",
        ".ufo/evidence/round-18/final/historical.stdout": "9050c284e68d6538ebedfc6a084fc0b4529fd50a691c72d9f7a4e570fa214590",
        ".ufo/evidence/round-18/final/probes.stdout": "d37c99e33eeb22b1b74b47b5fca26b228407792a5741bfaebc1b8be39aeb8cf0",
        ".ufo/evidence/round-18/final/registry-branch-aligned.stdout": "6502cb387613b08c64f0be73f41ff094575639f952ad1f2c4c8e76834d5517c4",
        ".ufo/evidence/round-18/final/regression.stdout": "226be3d529337dc87334b0e7c55a012fb0793865570565b84471aab6d836acfe",
        ".ufo/evidence/round-18/final/repeat.stdout": "9cd7809032b2a970bdc19577c57757e2d91e7e14f360cb37f5105eb3a0c3c21e"
      },
      "external_inputs": {},
      "traces": [
        ".ufo/evidence/round-18/coldread/traces/L1/audit-1707.json"
      ]
    },
    {
      "start": 1754,
      "heading": "## Seventh recorded case and full-page cold-read \u2014 round 16",
      "class": "instruction",
      "verdict": "gap-minor",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [
        "L1 residual verification is not a blind non-author cold read. Real command execution receipts are ancestor-pinned (921ef807/5923d89); the read revision adds only citation/receipt files and the D/N prose correction, not executable instruments. Historical per-run timestamps and deleted scratch logs remain record-only."
      ],
      "commands_executed": [
        "Pinned-source and committed actual-execution receipt audit: .ufo/evidence/round-18/coldread/traces/L1/audit-1754.json"
      ],
      "opened": [
        "corpus/knowledge/mutation-case-kumitate-round-gate.md",
        ".ufo/evidence/round-16/round-gate/predictions.json",
        ".ufo/evidence/round-16/round-gate/round-gate.defects.spec",
        "tools/mutate-and-run.sh",
        ".ufo/evidence/round-18/final/registry-branch-aligned.stdout",
        ".ufo/evidence/round-18/final/probes.stdout",
        ".ufo/evidence/round-18/final/regression.stdout",
        ".ufo/evidence/round-18/final/case8.stdout",
        ".ufo/evidence/round-18/final/case7.stdout",
        ".ufo/evidence/round-18/final/historical.stdout",
        ".ufo/evidence/round-18/final/context.stdout",
        ".ufo/evidence/round-18/final/disposition.stdout",
        ".ufo/evidence/round-18/final/before.stdout",
        ".ufo/evidence/round-18/final/repeat.stdout",
        ".ufo/evidence/round-18/final/checks.json"
      ],
      "inputs": {
        ".ufo/evidence/round-16/round-gate/predictions.json": "bb344eee3b034d774a829042717dc5c78517edcf8ef5f369831bc2fae0f70bc1",
        ".ufo/evidence/round-16/round-gate/round-gate.defects.spec": "e99b87ebc16f045f43ffb31354e2fc2879d2be3a8504d4274239249b93ef11c4",
        ".ufo/evidence/round-18/final/before.stdout": "e279b328de7d08631de687a0ad587943ca0a9eecba3c046adeb31b44f7a25b0d",
        ".ufo/evidence/round-18/final/case7.stdout": "e649866e5194fe54a6773582551e7fb83a33bafb0cfd661ba6b71bb8da9c7ceb",
        ".ufo/evidence/round-18/final/case8.stdout": "b4f264c375833f3c65d3ea00606851df58edc6c575617d4034f08ccfdf63694b",
        ".ufo/evidence/round-18/final/checks.json": "fed3c8e6cba05c41d8fdcafc091328e3092e2018a42fb8a8594bd8b5815c671d",
        ".ufo/evidence/round-18/final/context.stdout": "337aa6d8b19b2a82ed7de8854bf39a964076126c72bcc0b51798eca6bb134994",
        ".ufo/evidence/round-18/final/disposition.stdout": "596975d456657c8d683b6cae4382bdc958cda0084a2cd54d4b979957f55048e4",
        ".ufo/evidence/round-18/final/historical.stdout": "9050c284e68d6538ebedfc6a084fc0b4529fd50a691c72d9f7a4e570fa214590",
        ".ufo/evidence/round-18/final/probes.stdout": "d37c99e33eeb22b1b74b47b5fca26b228407792a5741bfaebc1b8be39aeb8cf0",
        ".ufo/evidence/round-18/final/registry-branch-aligned.stdout": "6502cb387613b08c64f0be73f41ff094575639f952ad1f2c4c8e76834d5517c4",
        ".ufo/evidence/round-18/final/regression.stdout": "226be3d529337dc87334b0e7c55a012fb0793865570565b84471aab6d836acfe",
        ".ufo/evidence/round-18/final/repeat.stdout": "9cd7809032b2a970bdc19577c57757e2d91e7e14f360cb37f5105eb3a0c3c21e",
        "corpus/knowledge/mutation-case-kumitate-round-gate.md": "1b907c8d2c756134783604b604b3dd0a65b0a5fcb0f5a82e5d24b037b82aeaec",
        "tools/mutate-and-run.sh": "d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b"
      },
      "external_inputs": {},
      "traces": [
        ".ufo/evidence/round-18/coldread/traces/L1/audit-1754.json"
      ]
    },
    {
      "start": 1814,
      "heading": "## Live-tree re-pin and entry-command monitor \u2014 round 17",
      "class": "instruction",
      "verdict": "gap-minor",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [
        "L1 residual verification is not a blind non-author cold read. Real command execution receipts are ancestor-pinned (921ef807/5923d89); the read revision adds only citation/receipt files and the D/N prose correction, not executable instruments. Historical per-run timestamps and deleted scratch logs remain record-only."
      ],
      "commands_executed": [
        "Pinned-source and committed actual-execution receipt audit: .ufo/evidence/round-18/coldread/traces/L1/audit-1814.json"
      ],
      "opened": [
        "tools/evidence-disposition.py",
        "tools/registry-check.py",
        "tools/registry.json",
        ".ufo/evidence/round-18/dispositions.json",
        ".ufo/evidence/round-18/dispositions-before.json",
        "tools/pin-disposition.py",
        ".ufo/evidence/round-18/final/registry-branch-aligned.stdout",
        ".ufo/evidence/round-18/final/probes.stdout",
        ".ufo/evidence/round-18/final/regression.stdout",
        ".ufo/evidence/round-18/final/case8.stdout",
        ".ufo/evidence/round-18/final/case7.stdout",
        ".ufo/evidence/round-18/final/historical.stdout",
        ".ufo/evidence/round-18/final/context.stdout",
        ".ufo/evidence/round-18/final/disposition.stdout",
        ".ufo/evidence/round-18/final/before.stdout",
        ".ufo/evidence/round-18/final/repeat.stdout",
        ".ufo/evidence/round-18/final/checks.json"
      ],
      "inputs": {
        ".ufo/evidence/round-18/dispositions-before.json": "dc948a5ee1bab7a89e21ef4d75b620a430559ae0b2b64573f7c2bcacbc4deb65",
        ".ufo/evidence/round-18/dispositions.json": "9caa2f76dcc36265bb11b58baa397b1015a91b086db63d203ab16020a1fc2676",
        ".ufo/evidence/round-18/final/before.stdout": "e279b328de7d08631de687a0ad587943ca0a9eecba3c046adeb31b44f7a25b0d",
        ".ufo/evidence/round-18/final/case7.stdout": "e649866e5194fe54a6773582551e7fb83a33bafb0cfd661ba6b71bb8da9c7ceb",
        ".ufo/evidence/round-18/final/case8.stdout": "b4f264c375833f3c65d3ea00606851df58edc6c575617d4034f08ccfdf63694b",
        ".ufo/evidence/round-18/final/checks.json": "fed3c8e6cba05c41d8fdcafc091328e3092e2018a42fb8a8594bd8b5815c671d",
        ".ufo/evidence/round-18/final/context.stdout": "337aa6d8b19b2a82ed7de8854bf39a964076126c72bcc0b51798eca6bb134994",
        ".ufo/evidence/round-18/final/disposition.stdout": "596975d456657c8d683b6cae4382bdc958cda0084a2cd54d4b979957f55048e4",
        ".ufo/evidence/round-18/final/historical.stdout": "9050c284e68d6538ebedfc6a084fc0b4529fd50a691c72d9f7a4e570fa214590",
        ".ufo/evidence/round-18/final/probes.stdout": "d37c99e33eeb22b1b74b47b5fca26b228407792a5741bfaebc1b8be39aeb8cf0",
        ".ufo/evidence/round-18/final/registry-branch-aligned.stdout": "6502cb387613b08c64f0be73f41ff094575639f952ad1f2c4c8e76834d5517c4",
        ".ufo/evidence/round-18/final/regression.stdout": "226be3d529337dc87334b0e7c55a012fb0793865570565b84471aab6d836acfe",
        ".ufo/evidence/round-18/final/repeat.stdout": "9cd7809032b2a970bdc19577c57757e2d91e7e14f360cb37f5105eb3a0c3c21e",
        "tools/evidence-disposition.py": "66655a3a692b587fd0a6dc3f2cf0edd766a824eb86280753d0bd57efeecc1f44",
        "tools/pin-disposition.py": "331529eadafe9138c88c1fe09666c9401d28c166f16bc92ecc092fc4d92c3a4c",
        "tools/registry-check.py": "33d0d17c140a6b9662c023a3a8cfa67065e17fb8c73af20d7c8055005565aeb6",
        "tools/registry.json": "3e6785ee90fcf75f7147ffdb8bee72ef0bce54343803604df857951cc279f1e6"
      },
      "external_inputs": {},
      "traces": [
        ".ufo/evidence/round-18/coldread/traces/L1/audit-1814.json"
      ]
    },
    {
      "start": 1846,
      "heading": "### Round-17 gate/probe registry \u2014 re-pin and monitor",
      "class": "instruction",
      "verdict": "gap-minor",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [
        "L1 residual verification is not a blind non-author cold read. Real command execution receipts are ancestor-pinned (921ef807/5923d89); the read revision adds only citation/receipt files and the D/N prose correction, not executable instruments. Historical per-run timestamps and deleted scratch logs remain record-only."
      ],
      "commands_executed": [
        "Pinned-source and committed actual-execution receipt audit: .ufo/evidence/round-18/coldread/traces/L1/audit-1846.json"
      ],
      "opened": [
        "tools/evidence-disposition.py",
        "tools/registry-check.py",
        "tools/mutate-and-run.sh",
        "tools/pin-disposition.py",
        "tools/registry.json",
        ".ufo/evidence/round-18/final/registry-branch-aligned.stdout",
        ".ufo/evidence/round-18/final/probes.stdout",
        ".ufo/evidence/round-18/final/regression.stdout",
        ".ufo/evidence/round-18/final/case8.stdout",
        ".ufo/evidence/round-18/final/case7.stdout",
        ".ufo/evidence/round-18/final/historical.stdout",
        ".ufo/evidence/round-18/final/context.stdout",
        ".ufo/evidence/round-18/final/disposition.stdout",
        ".ufo/evidence/round-18/final/before.stdout",
        ".ufo/evidence/round-18/final/repeat.stdout",
        ".ufo/evidence/round-18/final/checks.json"
      ],
      "inputs": {
        ".ufo/evidence/round-18/final/before.stdout": "e279b328de7d08631de687a0ad587943ca0a9eecba3c046adeb31b44f7a25b0d",
        ".ufo/evidence/round-18/final/case7.stdout": "e649866e5194fe54a6773582551e7fb83a33bafb0cfd661ba6b71bb8da9c7ceb",
        ".ufo/evidence/round-18/final/case8.stdout": "b4f264c375833f3c65d3ea00606851df58edc6c575617d4034f08ccfdf63694b",
        ".ufo/evidence/round-18/final/checks.json": "fed3c8e6cba05c41d8fdcafc091328e3092e2018a42fb8a8594bd8b5815c671d",
        ".ufo/evidence/round-18/final/context.stdout": "337aa6d8b19b2a82ed7de8854bf39a964076126c72bcc0b51798eca6bb134994",
        ".ufo/evidence/round-18/final/disposition.stdout": "596975d456657c8d683b6cae4382bdc958cda0084a2cd54d4b979957f55048e4",
        ".ufo/evidence/round-18/final/historical.stdout": "9050c284e68d6538ebedfc6a084fc0b4529fd50a691c72d9f7a4e570fa214590",
        ".ufo/evidence/round-18/final/probes.stdout": "d37c99e33eeb22b1b74b47b5fca26b228407792a5741bfaebc1b8be39aeb8cf0",
        ".ufo/evidence/round-18/final/registry-branch-aligned.stdout": "6502cb387613b08c64f0be73f41ff094575639f952ad1f2c4c8e76834d5517c4",
        ".ufo/evidence/round-18/final/regression.stdout": "226be3d529337dc87334b0e7c55a012fb0793865570565b84471aab6d836acfe",
        ".ufo/evidence/round-18/final/repeat.stdout": "9cd7809032b2a970bdc19577c57757e2d91e7e14f360cb37f5105eb3a0c3c21e",
        "tools/evidence-disposition.py": "66655a3a692b587fd0a6dc3f2cf0edd766a824eb86280753d0bd57efeecc1f44",
        "tools/mutate-and-run.sh": "d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b",
        "tools/pin-disposition.py": "331529eadafe9138c88c1fe09666c9401d28c166f16bc92ecc092fc4d92c3a4c",
        "tools/registry-check.py": "33d0d17c140a6b9662c023a3a8cfa67065e17fb8c73af20d7c8055005565aeb6",
        "tools/registry.json": "3e6785ee90fcf75f7147ffdb8bee72ef0bce54343803604df857951cc279f1e6"
      },
      "external_inputs": {},
      "traces": [
        ".ufo/evidence/round-18/coldread/traces/L1/audit-1846.json"
      ]
    },
    {
      "start": 1855,
      "heading": "## Input-keyed cold-read credit \u2014 round 17",
      "class": "instruction",
      "verdict": "gap-minor",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [
        "L1 residual verification is not a blind non-author cold read. Real command execution receipts are ancestor-pinned (921ef807/5923d89); the read revision adds only citation/receipt files and the D/N prose correction, not executable instruments. Historical per-run timestamps and deleted scratch logs remain record-only."
      ],
      "commands_executed": [
        "Pinned-source and committed actual-execution receipt audit: .ufo/evidence/round-18/coldread/traces/L1/audit-1855.json"
      ],
      "opened": [
        "corpus/knowledge/input-keyed-coldread-credit.md",
        ".ufo/evidence/round-18/measure.py",
        ".ufo/evidence/round-18/coldread/assemble.py",
        "tools/trace-inputs.py",
        ".ufo/evidence/round-18/final/registry-branch-aligned.stdout",
        ".ufo/evidence/round-18/final/probes.stdout",
        ".ufo/evidence/round-18/final/regression.stdout",
        ".ufo/evidence/round-18/final/case8.stdout",
        ".ufo/evidence/round-18/final/case7.stdout",
        ".ufo/evidence/round-18/final/historical.stdout",
        ".ufo/evidence/round-18/final/context.stdout",
        ".ufo/evidence/round-18/final/disposition.stdout",
        ".ufo/evidence/round-18/final/before.stdout",
        ".ufo/evidence/round-18/final/repeat.stdout",
        ".ufo/evidence/round-18/final/checks.json"
      ],
      "inputs": {
        ".ufo/evidence/round-18/coldread/assemble.py": "bf7c12f7b69dcdb004c7df546cd9655f6f1264ebb3e5565810a673c42dba5a0a",
        ".ufo/evidence/round-18/final/before.stdout": "e279b328de7d08631de687a0ad587943ca0a9eecba3c046adeb31b44f7a25b0d",
        ".ufo/evidence/round-18/final/case7.stdout": "e649866e5194fe54a6773582551e7fb83a33bafb0cfd661ba6b71bb8da9c7ceb",
        ".ufo/evidence/round-18/final/case8.stdout": "b4f264c375833f3c65d3ea00606851df58edc6c575617d4034f08ccfdf63694b",
        ".ufo/evidence/round-18/final/checks.json": "fed3c8e6cba05c41d8fdcafc091328e3092e2018a42fb8a8594bd8b5815c671d",
        ".ufo/evidence/round-18/final/context.stdout": "337aa6d8b19b2a82ed7de8854bf39a964076126c72bcc0b51798eca6bb134994",
        ".ufo/evidence/round-18/final/disposition.stdout": "596975d456657c8d683b6cae4382bdc958cda0084a2cd54d4b979957f55048e4",
        ".ufo/evidence/round-18/final/historical.stdout": "9050c284e68d6538ebedfc6a084fc0b4529fd50a691c72d9f7a4e570fa214590",
        ".ufo/evidence/round-18/final/probes.stdout": "d37c99e33eeb22b1b74b47b5fca26b228407792a5741bfaebc1b8be39aeb8cf0",
        ".ufo/evidence/round-18/final/registry-branch-aligned.stdout": "6502cb387613b08c64f0be73f41ff094575639f952ad1f2c4c8e76834d5517c4",
        ".ufo/evidence/round-18/final/regression.stdout": "226be3d529337dc87334b0e7c55a012fb0793865570565b84471aab6d836acfe",
        ".ufo/evidence/round-18/final/repeat.stdout": "9cd7809032b2a970bdc19577c57757e2d91e7e14f360cb37f5105eb3a0c3c21e",
        ".ufo/evidence/round-18/measure.py": "7ca87a7c98196d87a86627cf96e2e9bc7b3a8769496a75ce8caca1955b26dd37",
        "corpus/knowledge/input-keyed-coldread-credit.md": "0c45dccb4dfa78cdfd2dfddc59132d1e636ed0d548abcb9528d1b1aa21fd0636",
        "tools/trace-inputs.py": "fb1d81f67551fb04e9e447cbc706ef5cc9cfd5208169004184b24ab15f3f2636"
      },
      "external_inputs": {},
      "traces": [
        ".ufo/evidence/round-18/coldread/traces/L1/audit-1855.json"
      ]
    },
    {
      "start": 1905,
      "heading": "## Eighth recorded case \u2014 round 18",
      "class": "record",
      "verdict": "gap-minor",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [
        "L1 residual verification is not a blind non-author cold read. Real command execution receipts are ancestor-pinned (921ef807/5923d89); the read revision adds only citation/receipt files and the D/N prose correction, not executable instruments. Historical per-run timestamps and deleted scratch logs remain record-only."
      ],
      "commands_executed": [
        "Pinned-source and committed actual-execution receipt audit: .ufo/evidence/round-18/coldread/traces/L1/audit-1905.json"
      ],
      "opened": [
        "corpus/knowledge/mutation-case-kumitate-sources-check.md",
        "tools/mutate-and-run.sh",
        ".ufo/evidence/round-18/sources-check/sources-check.defects.spec",
        ".ufo/evidence/round-18/sources-check/predictions.json",
        ".ufo/evidence/round-18/sources-check/sweep/sweep.txt",
        ".ufo/evidence/round-18/final/registry-branch-aligned.stdout",
        ".ufo/evidence/round-18/final/probes.stdout",
        ".ufo/evidence/round-18/final/regression.stdout",
        ".ufo/evidence/round-18/final/case8.stdout",
        ".ufo/evidence/round-18/final/case7.stdout",
        ".ufo/evidence/round-18/final/historical.stdout",
        ".ufo/evidence/round-18/final/context.stdout",
        ".ufo/evidence/round-18/final/disposition.stdout",
        ".ufo/evidence/round-18/final/before.stdout",
        ".ufo/evidence/round-18/final/repeat.stdout",
        ".ufo/evidence/round-18/final/checks.json"
      ],
      "inputs": {
        ".ufo/evidence/round-18/final/before.stdout": "e279b328de7d08631de687a0ad587943ca0a9eecba3c046adeb31b44f7a25b0d",
        ".ufo/evidence/round-18/final/case7.stdout": "e649866e5194fe54a6773582551e7fb83a33bafb0cfd661ba6b71bb8da9c7ceb",
        ".ufo/evidence/round-18/final/case8.stdout": "b4f264c375833f3c65d3ea00606851df58edc6c575617d4034f08ccfdf63694b",
        ".ufo/evidence/round-18/final/checks.json": "fed3c8e6cba05c41d8fdcafc091328e3092e2018a42fb8a8594bd8b5815c671d",
        ".ufo/evidence/round-18/final/context.stdout": "337aa6d8b19b2a82ed7de8854bf39a964076126c72bcc0b51798eca6bb134994",
        ".ufo/evidence/round-18/final/disposition.stdout": "596975d456657c8d683b6cae4382bdc958cda0084a2cd54d4b979957f55048e4",
        ".ufo/evidence/round-18/final/historical.stdout": "9050c284e68d6538ebedfc6a084fc0b4529fd50a691c72d9f7a4e570fa214590",
        ".ufo/evidence/round-18/final/probes.stdout": "d37c99e33eeb22b1b74b47b5fca26b228407792a5741bfaebc1b8be39aeb8cf0",
        ".ufo/evidence/round-18/final/registry-branch-aligned.stdout": "6502cb387613b08c64f0be73f41ff094575639f952ad1f2c4c8e76834d5517c4",
        ".ufo/evidence/round-18/final/regression.stdout": "226be3d529337dc87334b0e7c55a012fb0793865570565b84471aab6d836acfe",
        ".ufo/evidence/round-18/final/repeat.stdout": "9cd7809032b2a970bdc19577c57757e2d91e7e14f360cb37f5105eb3a0c3c21e",
        ".ufo/evidence/round-18/sources-check/predictions.json": "5749a27a92c862278a2c77307496f2b80b3c6619c6125def0ea0066b7252d35f",
        ".ufo/evidence/round-18/sources-check/sources-check.defects.spec": "c8d24cb4b6b1a372543764fc27c9d16f65510a29fed1045bedb2863ce2408c91",
        ".ufo/evidence/round-18/sources-check/sweep/sweep.txt": "4ba2a595668439e6ca77bdb26fb462e71e88fe9079a50a77ea9e7d7ff2586097",
        "corpus/knowledge/mutation-case-kumitate-sources-check.md": "dd405bd364016819a7609a0fae7c5a987ad0e06872ff97328e4f5b1b171b96c6",
        "tools/mutate-and-run.sh": "d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b"
      },
      "external_inputs": {},
      "traces": [
        ".ufo/evidence/round-18/coldread/traces/L1/audit-1905.json"
      ]
    },
    {
      "start": 1925,
      "heading": "### Round-18 gate/probe registry \u2014 routed-defect closure",
      "class": "instruction",
      "verdict": "gap-minor",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [
        "L1 residual verification is not a blind non-author cold read. Real command execution receipts are ancestor-pinned (921ef807/5923d89); the read revision adds only citation/receipt files and the D/N prose correction, not executable instruments. Historical per-run timestamps and deleted scratch logs remain record-only."
      ],
      "commands_executed": [
        "Pinned-source and committed actual-execution receipt audit: .ufo/evidence/round-18/coldread/traces/L1/audit-1925.json"
      ],
      "opened": [
        "tools/registry-check.py",
        "tools/evidence-disposition.py",
        "tools/bash-witness-study.py",
        "tools/trace-inputs.py",
        ".ufo/evidence/round-18/defect-probes.py",
        ".ufo/evidence/round-18/measure.py",
        ".ufo/evidence/round-18/coldread/assemble.py",
        "tools/registry.json",
        ".ufo/evidence/round-18/final/registry-branch-aligned.stdout",
        ".ufo/evidence/round-18/final/probes.stdout",
        ".ufo/evidence/round-18/final/regression.stdout",
        ".ufo/evidence/round-18/final/case8.stdout",
        ".ufo/evidence/round-18/final/case7.stdout",
        ".ufo/evidence/round-18/final/historical.stdout",
        ".ufo/evidence/round-18/final/context.stdout",
        ".ufo/evidence/round-18/final/disposition.stdout",
        ".ufo/evidence/round-18/final/before.stdout",
        ".ufo/evidence/round-18/final/repeat.stdout",
        ".ufo/evidence/round-18/final/checks.json"
      ],
      "inputs": {
        ".ufo/evidence/round-18/coldread/assemble.py": "bf7c12f7b69dcdb004c7df546cd9655f6f1264ebb3e5565810a673c42dba5a0a",
        ".ufo/evidence/round-18/defect-probes.py": "99297d9645151dee948291638386f3e9189c7bab590bebda23de6e51dadebeaa",
        ".ufo/evidence/round-18/final/before.stdout": "e279b328de7d08631de687a0ad587943ca0a9eecba3c046adeb31b44f7a25b0d",
        ".ufo/evidence/round-18/final/case7.stdout": "e649866e5194fe54a6773582551e7fb83a33bafb0cfd661ba6b71bb8da9c7ceb",
        ".ufo/evidence/round-18/final/case8.stdout": "b4f264c375833f3c65d3ea00606851df58edc6c575617d4034f08ccfdf63694b",
        ".ufo/evidence/round-18/final/checks.json": "fed3c8e6cba05c41d8fdcafc091328e3092e2018a42fb8a8594bd8b5815c671d",
        ".ufo/evidence/round-18/final/context.stdout": "337aa6d8b19b2a82ed7de8854bf39a964076126c72bcc0b51798eca6bb134994",
        ".ufo/evidence/round-18/final/disposition.stdout": "596975d456657c8d683b6cae4382bdc958cda0084a2cd54d4b979957f55048e4",
        ".ufo/evidence/round-18/final/historical.stdout": "9050c284e68d6538ebedfc6a084fc0b4529fd50a691c72d9f7a4e570fa214590",
        ".ufo/evidence/round-18/final/probes.stdout": "d37c99e33eeb22b1b74b47b5fca26b228407792a5741bfaebc1b8be39aeb8cf0",
        ".ufo/evidence/round-18/final/registry-branch-aligned.stdout": "6502cb387613b08c64f0be73f41ff094575639f952ad1f2c4c8e76834d5517c4",
        ".ufo/evidence/round-18/final/regression.stdout": "226be3d529337dc87334b0e7c55a012fb0793865570565b84471aab6d836acfe",
        ".ufo/evidence/round-18/final/repeat.stdout": "9cd7809032b2a970bdc19577c57757e2d91e7e14f360cb37f5105eb3a0c3c21e",
        ".ufo/evidence/round-18/measure.py": "7ca87a7c98196d87a86627cf96e2e9bc7b3a8769496a75ce8caca1955b26dd37",
        "tools/bash-witness-study.py": "8dfaa25aa2713635e7363f60effb442a474ba3656d6cf2bb171c0c22432e3a12",
        "tools/evidence-disposition.py": "66655a3a692b587fd0a6dc3f2cf0edd766a824eb86280753d0bd57efeecc1f44",
        "tools/registry-check.py": "33d0d17c140a6b9662c023a3a8cfa67065e17fb8c73af20d7c8055005565aeb6",
        "tools/registry.json": "3e6785ee90fcf75f7147ffdb8bee72ef0bce54343803604df857951cc279f1e6",
        "tools/trace-inputs.py": "fb1d81f67551fb04e9e447cbc706ef5cc9cfd5208169004184b24ab15f3f2636"
      },
      "external_inputs": {},
      "traces": [
        ".ufo/evidence/round-18/coldread/traces/L1/audit-1925.json"
      ]
    },
    {
      "start": 1069,
      "heading": "### Triggers T1\u2013T3 and the re-pin rule",
      "class": "instruction",
      "verdict": "gap-minor",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [
        "L1 residual verification, not blind. Historical scratch timestamps remain uncorroborated; actual current regression passed and pinned case-7 RerunSweep record supports the corrected T2 precedent."
      ],
      "commands_executed": [
        "Pinned source plus actual execution-output audit: .ufo/evidence/round-18/coldread/traces/L1/audit-1069.json"
      ],
      "opened": [
        "corpus/knowledge/fleet-kill-rate-ledger.md",
        "corpus/knowledge/mutation-case-mado-verify.md",
        "corpus/knowledge/mutation-case-kumitate-round-gate.md",
        ".ufo/evidence/round-16/round-gate/runner-regression.txt",
        "tools/mutate-and-run.sh",
        ".ufo/evidence/round-18/final/registry-branch-aligned.stdout",
        ".ufo/evidence/round-18/final/probes.stdout",
        ".ufo/evidence/round-18/final/regression.stdout",
        ".ufo/evidence/round-18/final/case8.stdout",
        ".ufo/evidence/round-18/final/case7.stdout",
        ".ufo/evidence/round-18/final/historical.stdout",
        ".ufo/evidence/round-18/final/context.stdout",
        ".ufo/evidence/round-18/final/disposition.stdout",
        ".ufo/evidence/round-18/final/before.stdout",
        ".ufo/evidence/round-18/final/repeat.stdout",
        ".ufo/evidence/round-18/final/checks.json"
      ],
      "inputs": {
        ".ufo/evidence/round-16/round-gate/runner-regression.txt": "630c3806e106af550d4afc6cd79bf2b0846472530a33772038df443db6e591e4",
        ".ufo/evidence/round-18/final/before.stdout": "e279b328de7d08631de687a0ad587943ca0a9eecba3c046adeb31b44f7a25b0d",
        ".ufo/evidence/round-18/final/case7.stdout": "e649866e5194fe54a6773582551e7fb83a33bafb0cfd661ba6b71bb8da9c7ceb",
        ".ufo/evidence/round-18/final/case8.stdout": "b4f264c375833f3c65d3ea00606851df58edc6c575617d4034f08ccfdf63694b",
        ".ufo/evidence/round-18/final/checks.json": "fed3c8e6cba05c41d8fdcafc091328e3092e2018a42fb8a8594bd8b5815c671d",
        ".ufo/evidence/round-18/final/context.stdout": "337aa6d8b19b2a82ed7de8854bf39a964076126c72bcc0b51798eca6bb134994",
        ".ufo/evidence/round-18/final/disposition.stdout": "596975d456657c8d683b6cae4382bdc958cda0084a2cd54d4b979957f55048e4",
        ".ufo/evidence/round-18/final/historical.stdout": "9050c284e68d6538ebedfc6a084fc0b4529fd50a691c72d9f7a4e570fa214590",
        ".ufo/evidence/round-18/final/probes.stdout": "d37c99e33eeb22b1b74b47b5fca26b228407792a5741bfaebc1b8be39aeb8cf0",
        ".ufo/evidence/round-18/final/registry-branch-aligned.stdout": "6502cb387613b08c64f0be73f41ff094575639f952ad1f2c4c8e76834d5517c4",
        ".ufo/evidence/round-18/final/regression.stdout": "226be3d529337dc87334b0e7c55a012fb0793865570565b84471aab6d836acfe",
        ".ufo/evidence/round-18/final/repeat.stdout": "9cd7809032b2a970bdc19577c57757e2d91e7e14f360cb37f5105eb3a0c3c21e",
        "corpus/knowledge/fleet-kill-rate-ledger.md": "13a11e468dbf26972bb9734c2f0bedec859386f6729225c367c61ba056d7499e",
        "corpus/knowledge/mutation-case-kumitate-round-gate.md": "1b907c8d2c756134783604b604b3dd0a65b0a5fcb0f5a82e5d24b037b82aeaec",
        "corpus/knowledge/mutation-case-mado-verify.md": "f2d53d495e6c1d8b2c18e7bc0eac54955d477455958b10866c5f8712b2086bf3",
        "tools/mutate-and-run.sh": "d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b"
      },
      "external_inputs": {},
      "traces": [
        ".ufo/evidence/round-18/coldread/traces/L1/audit-1069.json"
      ]
    }
  ]
}
```
