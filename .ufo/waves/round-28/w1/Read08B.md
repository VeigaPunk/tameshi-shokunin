# Read08B — independent cold read, SKILL.md section at 1548 (rev b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a)

Section: lines 1548–1562, heading `### Round-13 gate/probe registry` (ends before `## Effective expectation reconciliation — round 14` at 1563; no code fences inside). Class: `record` — a registry stating facts with pointers (entry/self-test commands, pinned value paths), plus a scope-limiting prose note.

```json
{"schema": "tameshi-coldread-report-v2", "seat": "Read08B", "skill_sha256": "c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6", "read_rev": "b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a",
  "sections": [{"start": 1548, "heading": "### Round-13 gate/probe registry", "class": "record", "verdict": "gap-minor", "blocking_gaps": [], "wrong_expectations": [],
    "minor_gaps": [
      "Row-1 entry command (pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin) was not executed: its --root is the live fleet root, which contains the live lane, and cold-read bounds forbid reading the live lane under traces. Its verdict-map and selftest claims were verified instead by running the row's own --selftest (PASS 19/19) and reading the tool source.",
      "Row-2 verdict-map 'including usage' under exit 2 was verified by source inspection only (argparse parse_args at tools/witness-metadata.py:1249-1250, whose usage exit is 2), not by executing a usage-error invocation."
    ],
    "commands_executed": [
      "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/SOURCES.md tools/pin-disposition.py tools/witness-metadata.py .ufo/evidence/round-13/pin-manifest.json .ufo/evidence/round-13/expected.json .ufo/evidence/round-13/witness-metadata.json .ufo/evidence/round-13/producer-oracle-repair.json .ufo/evidence/round-13/pin-dispositions.json",
      "python3 tools/pin-disposition.py --selftest",
      "python3 tools/witness-metadata.py --selftest",
      "python3 tools/witness-metadata.py --check --companion .ufo/evidence/round-13/witness-metadata.json"
    ],
    "opened": [".ufo/evidence/round-12/BashWitness/declaration.json", ".ufo/evidence/round-12/BashWitness/declared.tsv", ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json", ".ufo/evidence/round-12/BashWitness/summary.json", ".ufo/evidence/round-13/expected.json", ".ufo/evidence/round-13/pin-dispositions.json", ".ufo/evidence/round-13/pin-manifest.json", ".ufo/evidence/round-13/producer-before.py", ".ufo/evidence/round-13/producer-oracle-repair.json", ".ufo/evidence/round-13/producer-oracle.py", ".ufo/evidence/round-13/verification.json", ".ufo/evidence/round-13/witness-metadata.json", "corpus/SOURCES.md", "tools/pin-disposition.py", "tools/witness-metadata.py"],
    "inputs": {
      ".ufo/evidence/round-12/BashWitness/declaration.json": "e8d2024ad13e021c5b7c41a66b881225beb9e0b30190833f0ab2310cf3670901",
      ".ufo/evidence/round-12/BashWitness/declared.tsv": "0def0d3b370288f58048c7dfb05aec652f9a262664e9f9ce27ae8fad5e6741d3",
      ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json": "6726421fde88e8d2aff4c9d0ff4a4fdce9b1d4651da50b89f2bf29f65a22a5f0",
      ".ufo/evidence/round-12/BashWitness/summary.json": "acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9",
      ".ufo/evidence/round-13/expected.json": "a016079438e96f39b2ef025052e786626bb553068fc0d2de93b96a09e5394336",
      ".ufo/evidence/round-13/pin-dispositions.json": "210850f51040fd11d5c63711417f72fb816171a55a23d82f52f7969be711a637",
      ".ufo/evidence/round-13/pin-manifest.json": "64eaa43e3f7a928472efa32c7230ca78358235716db04947a93edb0202920af6",
      ".ufo/evidence/round-13/producer-before.py": "592c5c3de86a684fbb694d3aa8dd4c1e2b62263e7a50d72a9169092ad3fab9a0",
      ".ufo/evidence/round-13/producer-oracle-repair.json": "df83a72994a93cd8d38c5c228ed85f2ed6d978ebb86a7fb260db51b34dfbef8d",
      ".ufo/evidence/round-13/producer-oracle.py": "d5ae0bd4d4f75a461e7105b63eb737d249c3d09ffc15a3bfeb7aecea21ccd38b",
      ".ufo/evidence/round-13/verification.json": "a02718e976382696b59f49e044b05af3d05fb0d5c964e4d218bfc6a2a033f06f",
      ".ufo/evidence/round-13/witness-metadata.json": "463282270a04bd46f4a0522ff6a349b77d268ede47725c4e1c52ca892210bd8d",
      "corpus/SOURCES.md": "a1624b7faaf17353d869ccf33cc811e53978e87115871cb449837561c3f85a45",
      "tools/pin-disposition.py": "331529eadafe9138c88c1fe09666c9401d28c166f16bc92ecc092fc4d92c3a4c",
      "tools/witness-metadata.py": "df3390682a04ccbb2469060c3deab924f9d8df72ce1a5b195d3618ce6cc0bed4"
    },
    "external_inputs": {},
    "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read08B-1.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read08B-2.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read08B-3.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read08B-4.json"]}]
}
```

What I checked (all inside a fresh /tmp fleet-mirror clone detached at b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a, working tree clean; SKILL.md sha256 matched the pinned page digest):

- Row 1 "six-leg content disposition" (probe, `tools/pin-disposition.py`): the row's self-test command ran under the collector — `SELFTEST: PASS (19/19)`, exit 0, all fixtures isolated under /tmp (`tempfile.mkdtemp(... dir="/tmp")`, docstring "no fleet repo, no sibling repo is read", tools/pin-disposition.py:704-706), matching the declared write scope. Verdict map confirmed against observed selftest cases and source: observation cases incl. changed/unavailable/missing expect exit 0; invalid-input cases (malformed digest, duplicate/missing leg, malformed JSON, missing manifest, invalid root) expect exit 2; "selftest 1 failed" matches the tool's convention (returns 1 on selftest FAIL at :1327, 0 on PASS at :1330). "Six-leg" confirmed: manifest `.ufo/evidence/round-13/pin-manifest.json` has exactly 6 legs, and the tool's canonical leg mapping + literal SELFTEST_CASE labels are in the tool. Pinned manifest exists at rev.
- Row 2 "exposed witness provenance companion" (gate, `tools/witness-metadata.py`): both named commands ran under the collector. `--check --companion .ufo/evidence/round-13/witness-metadata.json` → `WITNESS_METADATA: metadata_consistent reason=ok exit=0`, exactly the map's "0 metadata_consistent/clean". Selftest `SELFTEST: PASS 39/39` with 1 = metadata_inconsistent/*, 2 = input_unavailable|snapshot_tampered — matching the map. Pinned values confirmed: literal frozen round-12 BashWitness input digests live in the tool (the tool read them during selftest/check; digests recorded in `inputs`), and `.ufo/evidence/round-13/expected.json` holds `expected_checks` including `metadata_selftest` and `witness_check` (the companion's expected verdict).
- Prose: `verification.json`'s producer entry names `producer-before.py` with sha256 592c5c3d… which equals the actual file's digest — the historical summary's producer SHA names the producer that actually ran; the repaired producer `producer-oracle.py` (d5ae0bd4…, = `oracle_sha256` in producer-oracle-repair.json) appears only in a separate supersedes record, so no old evidence hash was regenerated. S048/S047 claim verified in corpus/SOURCES.md: S048 "supersedes S047 — item 4 is prioritisation rather than a reuse skip; no claim here resolves its pronoun to test versus mutation" (:57, noted again :255) — matching the section's quoted distinction and the no-pronoun-claim sentence.
- No blocking gaps, no wrong expectations found. Two minor verification gaps listed in the JSON (row-1 entry command not run — its `--root` names the live fleet/lane, off-bounds under traces; usage-exit-2 mapping checked by source inspection rather than execution).

No tools were installed or upgraded for this read. All commands ran in /tmp; nothing outside my report and the four trace receipts was written.

COLDREAD Read08B: gap-minor
