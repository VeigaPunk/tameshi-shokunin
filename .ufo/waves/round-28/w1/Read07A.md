# Read07A — cold read: "## Pin disposition and provenance correction — round 13" (SKILL.md:1517)

Read at detached clone rev b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a (SKILL.md sha256
c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6). Section runs
SKILL.md:1517–1562 (ends at `## Effective expectation reconciliation — round 14`,
line 1563); the `### Round-13 gate/probe registry` subheading is inside it.

```json
{"schema": "tameshi-coldread-report-v2", "seat": "Read07A", "skill_sha256": "c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6", "read_rev": "b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a",
  "sections": [{"start": 1517, "heading": "## Pin disposition and provenance correction — round 13", "class": "instruction", "verdict": "executed-ok", "blocking_gaps": [], "wrong_expectations": [],
    "minor_gaps": [],
    "commands_executed": [
      "python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin",
      "python3 tools/witness-metadata.py --check --companion .ufo/evidence/round-13/witness-metadata.json",
      "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/knowledge/incremental-pin-disposition.md corpus/lessons/round-12-verifier-spotcheck.md .ufo/evidence/round-13/pin-dispositions.json .ufo/evidence/round-13/expected.json .ufo/evidence/round-13/witness-metadata.json .ufo/evidence/round-13/verification-verdict.json",
      "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" .ufo/evidence/round-13/pin-dispositions.json .ufo/evidence/round-13/expected.json .ufo/evidence/round-13/verification-verdict.json .ufo/evidence/round-13/verification.json",
      "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/lessons/round-12-verifier-spotcheck.md corpus/SOURCES.md"
    ],
    "opened": [
      "tools/pin-disposition.py",
      "tools/witness-metadata.py",
      ".ufo/evidence/round-13/pin-manifest.json",
      ".ufo/evidence/round-13/witness-metadata.json",
      ".ufo/evidence/round-13/pin-dispositions.json",
      ".ufo/evidence/round-13/expected.json",
      ".ufo/evidence/round-13/verification-verdict.json",
      ".ufo/evidence/round-13/verification.json",
      ".ufo/evidence/round-12/BashWitness/declaration.json",
      ".ufo/evidence/round-12/BashWitness/declared.tsv",
      ".ufo/evidence/round-12/BashWitness/summary.json",
      ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json",
      "corpus/knowledge/incremental-pin-disposition.md",
      "corpus/lessons/round-12-verifier-spotcheck.md",
      "corpus/SOURCES.md"
    ],
    "inputs": {
      "tools/pin-disposition.py": "331529eadafe9138c88c1fe09666c9401d28c166f16bc92ecc092fc4d92c3a4c",
      "tools/witness-metadata.py": "df3390682a04ccbb2469060c3deab924f9d8df72ce1a5b195d3618ce6cc0bed4",
      ".ufo/evidence/round-13/pin-manifest.json": "64eaa43e3f7a928472efa32c7230ca78358235716db04947a93edb0202920af6",
      ".ufo/evidence/round-13/witness-metadata.json": "463282270a04bd46f4a0522ff6a349b77d268ede47725c4e1c52ca892210bd8d",
      ".ufo/evidence/round-13/pin-dispositions.json": "210850f51040fd11d5c63711417f72fb816171a55a23d82f52f7969be711a637",
      ".ufo/evidence/round-13/expected.json": "a016079438e96f39b2ef025052e786626bb553068fc0d2de93b96a09e5394336",
      ".ufo/evidence/round-13/verification-verdict.json": "1d128a44e0417eb29ca75195bc7f97b8d0ceae246f520710faf67c397ef35a4c",
      ".ufo/evidence/round-13/verification.json": "a02718e976382696b59f49e044b05af3d05fb0d5c964e4d218bfc6a2a033f06f",
      ".ufo/evidence/round-12/BashWitness/declaration.json": "e8d2024ad13e021c5b7c41a66b881225beb9e0b30190833f0ab2310cf3670901",
      ".ufo/evidence/round-12/BashWitness/declared.tsv": "0def0d3b370288f58048c7dfb05aec652f9a262664e9f9ce27ae8fad5e6741d3",
      ".ufo/evidence/round-12/BashWitness/summary.json": "acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9",
      ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json": "6726421fde88e8d2aff4c9d0ff4a4fdce9b1d4651da50b89f2bf29f65a22a5f0",
      "corpus/knowledge/incremental-pin-disposition.md": "0cc87300978412e774c8768936dbbac08fe90581da762bfd5a8f20fbd6fcf0b9",
      "corpus/lessons/round-12-verifier-spotcheck.md": "6ec29ffdf3bbe2f5bbcda3405a6e0ba51c2f5d02467c681d7c892edb3feafe30",
      "corpus/SOURCES.md": "a1624b7faaf17353d869ccf33cc811e53978e87115871cb449837561c3f85a45"
    },
    "external_inputs": {},
    "traces": [
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read07A-1.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read07A-2.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read07A-3.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read07A-4.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read07A-5.json"
    ]}]}
```

What I checked:

- **Class `instruction`** — the section's recipe names two runnable commands; both ran as written from the clone root.
- **Probe (recipe step 2):** `pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin` exited 0 and emitted `pin-disposition-v1` with `result_reuse=not_established` on every leg — matching the registry verdict map ("0 observations, including changed/unavailable") and the table rule "All three content identities agree → keep `result_reuse=not_established`". Today's observation is 1 unchanged / 5 changed; the frozen round-13 receipt `pin-dispositions.json` reads 3 unchanged / 3 changed — that is expected substrate drift since 2026-10-20, not a contradiction (the probe is explicitly a dated reading, not a verdict cache). It executed no sibling gate and wrote nothing (read-only, as claimed).
- **Gate (recipe step 3):** `witness-metadata.py --check --companion .ufo/evidence/round-13/witness-metadata.json` printed `metadata_consistent reason=ok` and exited 0 — matching verdict map "0 metadata_consistent/clean". Its traced inputs are exactly the round-12 BashWitness summary, declaration, declared.tsv and rerun summary plus the companion — consistent with the section's claims that originals keep their historical nulls while the companion normalizes only the canonical summary.
- **Claims cross-checked against opened records:** the S047 precision-correction row and S048 supersession claim match `corpus/SOURCES.md` rows (S047 supersedes S041; S048 gives the object-neutral "item 4 is prioritisation, not a reuse skip" distinction) and the knowledge entry `corpus/knowledge/incremental-pin-disposition.md`, which carries the same correction chain. `corpus/lessons/round-12-verifier-spotcheck.md` Routed defects item 3 exists and is exactly the defect this section discharges (append-only correction; `declaration.kind=null` repaired via a new companion, frozen declaration untouched).
- **No overclaim spotted:** the section claims no seventh case, no re-pin transfer, no rerun of sibling gates; the observed outputs carry the same limits (`not_compared` list, `result_reuse=not_established`).
- Note: one tracer-wrapped read (`Read07A-3.json`) exited 1 because I piped the reader through `head` and it hit BrokenPipeError after printing the first file — receipt still correctly records the inputs; the same files were re-read under clean receipts Read07A-4/5.
- Tool installs/updates: none.
COLDREAD Read07A: executed-ok
