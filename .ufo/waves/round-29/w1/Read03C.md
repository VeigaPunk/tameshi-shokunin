# Read03C — cold read of `### The map — where a reader enters, artifact by artifact` (SKILL.md:1380)

```json
{"schema": "tameshi-coldread-report-v2", "seat": "Read03C", "skill_sha256": "c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6", "read_rev": "9f3084bc60ad56aac01e4556ef4c7653df2f65e5",
  "sections": [{"start": 1380, "heading": "### The map — where a reader enters, artifact by artifact", "class": "record", "verdict": "gap-minor", "blocking_gaps": [], "wrong_expectations": [],
    "minor_gaps": ["Four of nine mutation-case notes carry the reproduction material inside other sections rather than a literal 'Reproduce' section (mado-verify §8 'Recommendation to the owner' body; round-gate §5, sources-check §5, cite-check §5 'Ledger leg'), so 'reproduce sections' holds only as a loose content summary, and sources-check's survivor probes are still PENDING at this rev — section exists, probes not executed.", "'Boundaries' in the service-optin-protocol row is met by §2 read-only guarantees + §3 owner-hardens rather than a named boundaries item — loose wording, substance holds."],
    "commands_executed": [
      "W=$(mktemp -d /tmp/Read03C-XXXX); mkdir $W/fleet; for d in /home/vgpnk/Projects/shokunin/*-shokunin; do b=$(basename $d); [ $b = tameshi-shokunin ] || ln -s $d $W/fleet/$b; done; git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin $W/fleet/tameshi-shokunin; git -C $W/fleet/tameshi-shokunin checkout -q --detach 9f3084bc60ad56aac01e4556ef4c7653df2f65e5  [setup; outside collector — creates the trace root]",
      "sha256sum /tmp/Read03C-qGwL/fleet/tameshi-shokunin/SKILL.md; git -C /tmp/Read03C-qGwL/fleet/tameshi-shokunin log -1 --format=%H; sed -n '1380,1520p' /tmp/Read03C-qGwL/fleet/tameshi-shokunin/SKILL.md",
      "sha256sum /tmp/Read03C-qGwL/fleet/tameshi-shokunin/tools/mutate-and-run.sh; sed -n '1294,1300p;1332,1346p;1355,1365p;1015,1020p' /tmp/Read03C-qGwL/fleet/tameshi-shokunin/SKILL.md",
      "sed -n '200,240p;304,330p' /tmp/Read03C-qGwL/fleet/tameshi-shokunin/.ufo/waves/round-26/w1/ColdreadPilot.md",
      "sed -n '1290,1300p' /tmp/Read03C-qGwL/fleet/tameshi-shokunin/SKILL.md",
      "sed -n '965,1008p;1021,1053p;1069,1090p;1230,1244p;1246,1271p;1324,1331p;1359,1363p' /tmp/Read03C-qGwL/fleet/tameshi-shokunin/SKILL.md",
      "python3 tools/trace-inputs.py --root /tmp/Read03C-qGwL/fleet/tameshi-shokunin --out .../Read03C-1.json -- python3 -c \"import sys,hashlib;[print(p, hashlib.sha256(open(p,'rb').read()).hexdigest()) for p in sys.argv[1:]]\" corpus/knowledge/operator-runbook.md corpus/knowledge/fleet-kill-rate-ledger.md corpus/knowledge/service-limits.md corpus/knowledge/service-optin-protocol.md corpus/knowledge/fleet-suite-census.md corpus/knowledge/service-standing-state.md corpus/knowledge/closeout-r11.md",
      "python3 tools/trace-inputs.py --root /tmp/Read03C-qGwL/fleet/tameshi-shokunin --out .../Read03C-2.json -- python3 -c \"import sys,hashlib;[print(p, hashlib.sha256(open(p,'rb').read()).hexdigest()) for p in sys.argv[1:]]\" corpus/knowledge/mutation-case-kimi-census.md corpus/knowledge/mutation-case-kagi-census.md corpus/knowledge/mutation-case-mado-verify.md corpus/knowledge/mutation-case-kagi-checklist.md corpus/knowledge/mutation-case-tsukuroi-census.md corpus/knowledge/mutation-case-kumitate-claims.md corpus/knowledge/mutation-case-kumitate-round-gate.md corpus/knowledge/mutation-case-kumitate-sources-check.md corpus/knowledge/mutation-case-kumitate-cite-check.md",
      "python3 tools/trace-inputs.py --root /tmp/Read03C-qGwL/fleet/tameshi-shokunin --out .../Read03C-3.json -- python3 -c \"import sys,hashlib;[print(p, hashlib.sha256(open(p,'rb').read()).hexdigest()) for p in sys.argv[1:]]\" corpus/README.md tools/mutate-and-run.sh",
      "python3 tools/trace-inputs.py --root /tmp/Read03C-qGwL/fleet/tameshi-shokunin --out .../Read03C-4.json -- python3 -c \"import sys,hashlib;[print(p, hashlib.sha256(open(p,'rb').read()).hexdigest()) for p in sys.argv[1:]]\" plans/round-4.plan.md plans/round-4-record-draft.md plans/round-5.plan.md plans/round-5-record-draft.md plans/round-6.plan.md plans/round-6-record-draft.md plans/round-7.plan.md plans/round-7-record-draft.md plans/round-8.plan.md plans/round-8-record-draft.md plans/round-9.plan.md plans/round-9-record-draft.md plans/round-10.plan.md plans/round-10-record-draft.md plans/round-11.plan.md plans/completion-evidence.md",
      "python3 tools/trace-inputs.py --root /tmp/Read03C-qGwL/fleet/tameshi-shokunin --out .../Read03C-5.json -- git ls-tree --name-only 9f3084bc60ad56aac01e4556ef4c7653df2f65e5 plans/",
      "python3 tools/trace-inputs.py --root /tmp/Read03C-qGwL/fleet/tameshi-shokunin --out .../Read03C-6.json -- git log --diff-filter=A --format=%h_%ad_%s --date=short --name-status -- 'corpus/knowledge/mutation-case-*.md'",
      "GIT_OPTIONAL_LOCKS=0 git -C /tmp/Read03C-qGwL/fleet/tameshi-shokunin show 9f3084bc60ad56aac01e4556ef4c7653df2f65e5:LOG.md | sha256sum  [excluded-file exception; outside collector]",
      "GIT_OPTIONAL_LOCKS=0 git -C /tmp/Read03C-qGwL/fleet/tameshi-shokunin show 9f3084bc60ad56aac01e4556ef4c7653df2f65e5:SCORECARD.md | sha256sum  [excluded-file exception; outside collector]",
      "GIT_OPTIONAL_LOCKS=0 git -C /tmp/Read03C-qGwL/fleet/tameshi-shokunin show 9f3084bc60ad56aac01e4556ef4c7653df2f65e5:LOG.md | sed -n '312,320p'  [excluded-file exception; outside collector]",
      "GIT_OPTIONAL_LOCKS=0 git -C /tmp/Read03C-qGwL/fleet/tameshi-shokunin show 9f3084bc60ad56aac01e4556ef4c7653df2f65e5:SCORECARD.md | sed -n '1,25p'  [excluded-file exception; outside collector]",
      "python3 tools/trace-inputs.py --root /tmp/Read03C-qGwL/fleet/tameshi-shokunin --out .../Read03C-7.json -- bash -c 'grep -n \"byte-frozen\\|never edited\\|frozen\" corpus/knowledge/fleet-kill-rate-ledger.md; sed -n \"168,174p\" corpus/knowledge/fleet-kill-rate-ledger.md; grep -n \"boundar\\|re-pin\" corpus/knowledge/service-optin-protocol.md | head -8; grep -n \"offer\\|queue\" corpus/knowledge/fleet-suite-census.md | head -8; for f in corpus/knowledge/mutation-case-*.md; do grep -icn reproduce \"$f\"; done; grep -n \"Round-29\\|round-29\" corpus/README.md | head; sed -n \"1,20p\" plans/completion-evidence.md; sed -n \"55,65p\" corpus/knowledge/service-optin-protocol.md'",
      "python3 tools/trace-inputs.py --root /tmp/Read03C-qGwL/fleet/tameshi-shokunin --out .../Read03C-8.json -- bash -c 'head -60 corpus/README.md; wc -l corpus/README.md; grep -n \"^#\" corpus/knowledge/operator-runbook.md; grep -n \"^#\" corpus/knowledge/fleet-kill-rate-ledger.md | head -20; grep -n \"^#\" corpus/knowledge/service-limits.md; grep -n \"^#\" corpus/knowledge/service-optin-protocol.md | head -20; grep -n \"^#\" corpus/knowledge/fleet-suite-census.md | head -15; grep -n \"^#\\|SC[0-9]\" corpus/knowledge/service-standing-state.md | head -20; for f in corpus/knowledge/mutation-case-*.md; do grep -n \"^#\" \"$f\"; done; grep -n \"git show <rev>:<path>\\|six legs\\|seven\\|eight\\|nine\" tools/mutate-and-run.sh | head -20; grep -n \"|\" corpus/knowledge/fleet-kill-rate-ledger.md | sed -n \"2,8p\"; sed -n \"214,235p;304,320p\" .ufo/waves/round-26/w1/ColdreadPilot.md; sha256sum .ufo/waves/round-26/w1/ColdreadPilot.md tools/trace-inputs.py'"],
    "opened": ["corpus/knowledge/operator-runbook.md", "corpus/knowledge/fleet-kill-rate-ledger.md", "corpus/knowledge/service-limits.md", "corpus/knowledge/service-optin-protocol.md", "corpus/knowledge/fleet-suite-census.md", "corpus/knowledge/service-standing-state.md", "corpus/knowledge/closeout-r11.md", "corpus/knowledge/mutation-case-kimi-census.md", "corpus/knowledge/mutation-case-kagi-census.md", "corpus/knowledge/mutation-case-mado-verify.md", "corpus/knowledge/mutation-case-kagi-checklist.md", "corpus/knowledge/mutation-case-tsukuroi-census.md", "corpus/knowledge/mutation-case-kumitate-claims.md", "corpus/knowledge/mutation-case-kumitate-round-gate.md", "corpus/knowledge/mutation-case-kumitate-sources-check.md", "corpus/knowledge/mutation-case-kumitate-cite-check.md", "corpus/README.md", "tools/mutate-and-run.sh", "tools/trace-inputs.py", ".ufo/waves/round-26/w1/ColdreadPilot.md", "plans/round-4.plan.md", "plans/round-4-record-draft.md", "plans/round-5.plan.md", "plans/round-5-record-draft.md", "plans/round-6.plan.md", "plans/round-6-record-draft.md", "plans/round-7.plan.md", "plans/round-7-record-draft.md", "plans/round-8.plan.md", "plans/round-8-record-draft.md", "plans/round-9.plan.md", "plans/round-9-record-draft.md", "plans/round-10.plan.md", "plans/round-10-record-draft.md", "plans/round-11.plan.md", "plans/completion-evidence.md", "SKILL.md"],
    "inputs": {"corpus/knowledge/operator-runbook.md": "8b2e185ff011f6cfc2aee187ff1c2a1f8120e410c00f4b67eb6c7f1ebabb6859", "corpus/knowledge/fleet-kill-rate-ledger.md": "13a11e468dbf26972bb9734c2f0bedec859386f6729225c367c61ba056d7499e", "corpus/knowledge/service-limits.md": "4fa8f039cdc446e63cf82dde9d9e718fafe4f85e212b8100f02706bec35730f0", "corpus/knowledge/service-optin-protocol.md": "84d0c1547eed257d921b832468d6f010bcca331e8ce67ed378852d7993da8e0e", "corpus/knowledge/fleet-suite-census.md": "ec1c2d8d2877a21df9752a7b20e6c307a144442a583ec6e6e03349d98ac94e4f", "corpus/knowledge/service-standing-state.md": "d326c1a4d61c97051db07c55fb6de69bdc4faa9bbef21186d0dc0451efafb952", "corpus/knowledge/closeout-r11.md": "cea3352aa60eb51b51e2722fdb820cac19cd1514670df931212904e826940265", "corpus/knowledge/mutation-case-kimi-census.md": "034524eff8f19cb8fca78cd5d13c6da9971f2ef2b5bedc1b950309c95c121548", "corpus/knowledge/mutation-case-kagi-census.md": "d3190a9940b9d47b7aae0025b2f4c80228d5a15cbb052cbef316ddff021d0bb0", "corpus/knowledge/mutation-case-mado-verify.md": "f2d53d495e6c1d8b2c18e7bc0eac54955d477455958b10866c5f8712b2086bf3", "corpus/knowledge/mutation-case-kagi-checklist.md": "43da70e675b8a482c942fddf6360d84970cf0c29ee648039e11b3b819ae739e7", "corpus/knowledge/mutation-case-tsukuroi-census.md": "b431bc6ce2b53e4ec05aa916ee51d279616716acdaa8f5ed72b83707a7fa9604", "corpus/knowledge/mutation-case-kumitate-claims.md": "3da1312e0a624ca565dc243fd0cb6f19968c1672f57066fbd4d2ad2bdf8045d9", "corpus/knowledge/mutation-case-kumitate-round-gate.md": "1b907c8d2c756134783604b604b3dd0a65b0a5fcb0f5a82e5d24b037b82aeaec", "corpus/knowledge/mutation-case-kumitate-sources-check.md": "d961a0d6645541ebec116d7a12f958426ac4561cd09e9adb6f09c9554afeea38", "corpus/knowledge/mutation-case-kumitate-cite-check.md": "a58bc159ef5b7eed9b42ad40c57a2c46d6ebfc898f530dbde790afc5f03fd34e", "corpus/README.md": "91c782f6803a30f26734793f73733e58bb6afc117965e06cbe4c625b88fd3c67", "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de", "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4", ".ufo/waves/round-26/w1/ColdreadPilot.md": "428a61a30ff8cf9e02f5a2a0923f916cf5f4c98596d2ace022f9d982fc25ceb7", "plans/round-4.plan.md": "4e63256474d56ba09a3d1e27298dc67cc45c3a60bc5daf70638a6f7b584d9e42", "plans/round-4-record-draft.md": "c142ccca8a44902e8dad9cefe5714c7255cc35dab80b17b5b3bb940361ac0cf9", "plans/round-5.plan.md": "5ade0413bc9a8d891df774156e597f893617ff80a49b4fe274adc204b8a63582", "plans/round-5-record-draft.md": "176d0d909898749a99b2cb71e061c594536b12da493d4e36f2ffc42c8df4a5e5", "plans/round-6.plan.md": "ec5b8236a1f12f57a83b45d24f77fbd9313894ae1305623404e2a9c4b7d86907", "plans/round-6-record-draft.md": "d146cc6171dc3e60b45a130fd29a0501269bd2272e467b0a1faab28c5696315e", "plans/round-7.plan.md": "49cd55fd0efaf892c281ec90538310cd5691af2af4ab1270c9945146fdc0fcec", "plans/round-7-record-draft.md": "9fed2565ca13ea63c5b23e81db01b4458e67db22aeef8791461cc8d3eb72eb2f", "plans/round-8.plan.md": "7e53c9d89b4887a482816639c6678346e8ed500137eefbcae6cac8997cc0358e", "plans/round-8-record-draft.md": "20218607d817f7fe456794da677dba2ce83439aa871a83697effc034e724235d", "plans/round-9.plan.md": "230ed6b61e4c89d9a0ad8c693dbf35a4368f137060f6ac0d3d8863433020da6a", "plans/round-9-record-draft.md": "0ca3094d0dc885022dcdf3c2b3e261188473d8e1633697ee65b17fdc56621ac7", "plans/round-10.plan.md": "d130596ac8bc7e91a0895ec8f4980166ce6303f4349b08830936dcf9e794a419", "plans/round-10-record-draft.md": "8020f9bda420646936047c49307bce4ec124d18b88fc83b14a15072902fad9fd", "plans/round-11.plan.md": "068578f198367b79b14fea95d9db550828908e345e5cbc161cabf0e4bea744f7", "plans/completion-evidence.md": "8e0485655a4801b9070bfa7dd688e774fed1a2e8b1692b046109ad83ebe2a3ef"},
    "external_inputs": {"tameshi-shokunin@9f3084bc60ad56aac01e4556ef4c7653df2f65e5:LOG.md": "b382162a10aa8264571fb067bca41de5e2abbe3dcbf5abe5282b1e0e1e736605", "tameshi-shokunin@9f3084bc60ad56aac01e4556ef4c7653df2f65e5:SCORECARD.md": "004a411d7af71e1977d619f4ef72aba40c9b9db1059b4f2e7d34da023a98dbac"},
    "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read03C-1.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read03C-2.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read03C-3.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read03C-4.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read03C-5.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read03C-6.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read03C-7.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read03C-8.json"]}]}
```

## What I checked

The section is lines 1380–1395 at the read revision: the heading plus an
eleven-row artifact table, ending before the `###` at line 1396. Class `record`
— it states what each artifact holds and when to read it; it does not tell the
reader to run anything.

All reads ran in a fleet-mirror clone (`/tmp/Read03C-qGwL/fleet/tameshi-shokunin`,
detached at `9f3084bc60ad56aac01e4556ef4c7653df2f65e5`; SKILL.md sha256 verified
`c46ec02e…`). Row-by-row:

- **operator-runbook row** — the note's headings carry §0 quick start (line 35),
  §2 the tool (93), §3 the six-case ledger (131), §4 opt-in (180), §5 limits
  (243), §6 the cadence with "the tick, the reading map, the triggers" (269),
  §7 regression mode (345), §10 unknowns (462). The pointer rule at SKILL.md
  `:1294-1297` was confirmed verbatim ("where it and an anchored source diverge,
  the anchored source governs" sits at SKILL.md:1294-1296).
- **ledger row** — `fleet-kill-rate-ledger.md` rows carry suite, rate +
  composition, survivors, hardened, and "Last sweep · target pin · driver"
  (sampled rows 1–4); §1–§4 are the measured/adjacent/queue/readings sections
  and later material is appended below (## Round 16 — seventh row appended,
  ## Round 18 — eighth row appended); ledger text itself says new rows land "as
  an appended row, not an edit of §1–§4" (line ~173). "Byte-frozen" is the
  map's compression of that; the mechanism (append-only §1–§4) is real.
- **service-limits row** — the note is the refusal detail of record (§1 decision
  table + §2 row detail); SKILL.md:1246-1270 is the compact rendering (a–j
  refusal table, ends at 1270, blank 1271, next heading at 1272). Confirmed.
- **service-optin-protocol row** — §1 request shape, the re-pin rule verbatim at
  line 62, §2 read-only guarantees, §4 report shape; "boundaries" rides on §3
  owner-hardens/stop-condition material rather than a named item (minor
  looseness, listed).
- **fleet-suite-census row** — §5 is "Tameshi's standing service offer"; "queue"
  appears as the unmeasured gate queue throughout; consistent.
- **service-standing-state row** — §1 fleet-visible vs §2 lane-owned, §3 handoff
  conditions, SC1/SC2/SC3 at §4 lines 159/174/181. Exact.
- **mutation-case row** — git log --diff-filter=A shows the adds exactly match
  "six at round 11; seven since round 16; eight since round 18; nine since round
  26" (six notes land by 2026-10-14 round-8 commit `c611d5d`; round-gate added
  in round-16 `c699c8c`; sources-check in round-18 `58e5d53`; cite-check in
  round-26 `40a12bf`). All nine hold spec/verdict/survivor material. The looseness:
  only four notes have a literal "## Reproduce" heading; mado, round-gate,
  sources-check and cite-check fold reproduction into other sections, and
  sources-check's survivor probes read "PENDING" at this rev. Recorded as a
  minor gap, not blocking — the map's description is of content, and the
  ledger-leg sections do carry the specs.
- **tools/mutate-and-run.sh row** — `--selftest`/`--regression` in usage; the
  header says verbatim "--regression (r4-2; r7-1 leg ledger; r10-2 six legs; r16
  seven; r18 eight; r26 nine)" and "All nine defect specs are embedded below";
  legs materialize "from its repo's git object store (`git show <rev>:<path>`)"
  (lines 10, 83, 108, 116; `regression_specs` writes nine specs at line 657).
  Exact.
- **corpus/README.md row** — "## Coverage map" table with Note/Holds/Sources
  columns, one row per note; the file also carries a round-29 frontier/predicate
  block at lines 444-446 (the monitor's `input-drift` reason — the drift is real
  but the row's description still holds at this rev).
- **plans row** — ls-tree at the rev shows plans+records for rounds 4–10 (plans
  also exist for rounds 2–3, consistent with "(rounds 4–10)" naming the
  record-draft convention); no `round-11-record` file exists; `plans/round-11.plan.md`
  and `plans/completion-evidence.md` both exist, and the pack's head says it
  collects "one line per round … the SHONEN status, and the debts". The cited
  LOG.md anchor: LOG.md:316-317 reads "the lane deliverables in this repo ARE
  the wave record (no `.ufo/waves/tameshi-r11-*` directory)" — checked via
  `git show` (LOG.md is an excluded file; read outside the collector per the
  exception and recorded in `external_inputs`). `closeout-r11.md` exists.
- **LOG.md / SCORECARD.md row** — via `git show` (excluded): LOG.md contains the
  round rows; SCORECARD.md "## Move log" rows carry counting commands per row
  (`git show … | wc -l`, `grep -cE` …). Both confirmed.

Monitor reason `input-drift:corpus/README.md` noted: the README at this rev
contains the round-29 block (lines 444-446); the map row's description of it is
unaffected.

Tooling: nothing installed (no pacman — host-wide pause; no tools needed beyond
python3/git/coreutils already present). Lane write surface used: trace receipts
only, plus this report.

COLDREAD Read03C: gap-minor
