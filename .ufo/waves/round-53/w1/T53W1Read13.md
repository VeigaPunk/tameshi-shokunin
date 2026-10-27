# T53W1Read13 — cold read of `### Round-13 gate/probe registry`

- Content commit read: `a41195dfc13a73958e4c5228ec196b28d03ded03` (git objects only; the working tree was not used for section text).
- Section: SKILL.md lines 1555–1568 (next heading at 1569, `## Effective expectation reconciliation — round 14`), 14 lines.
- `section_sha256` = `cfe1211232579bcfe7195d81b3932f2bc08109b30d58a3c853f2aff608514e50`

## Split verification (frozen monitor definition)

- Heading match outside fences: `^#{1,3}(\s|$)` over `git show C*:SKILL.md`, line 1555 is the only line equal to the heading; `git show C*:SKILL.md | grep -n '^#\{1,3\}\([[:space:]]\|$\)' | grep -i 'round-13'` printed `1555:### Round-13 gate/probe registry`.
- Section = heading line through the line before the next heading, trailing whitespace-only lines stripped, joined with `\n`, no trailing newline; last section line is `is needed by this method.`
- The digest was computed twice by independent code paths (line-split walk and direct slice of `lines[1554:1568]`); both returned `cfe12112…c514e50` over UTF-8/surrogateescape bytes.
- `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show a41195dfc13a73958e4c5228ec196b28d03ded03:SKILL.md > SKILL.md` then `sha256sum SKILL.md` gave `c329d3c150200ff32c47cb218800fb87c014345a7f342e1b11c70f5cacfc83ee` (whole file, 2178 lines).

The C* tree was exported read-only into scratch for execution: `git -C …/tameshi-shokunin archive C* | tar -x` under `/fast/scratch/hyaku/tameshi-r53/w1/T53W1Read13/tree`; every command below ran from that export with `TMPDIR` set to the same scratch root.

## Checks run and holds

1. **Row 1 entry command (probe).** `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin` → exit 0, `"status": "ok"`, `{"legs": 6, "unchanged": 1, "changed": 5, "unavailable": 0}`. Matches the map's "0 observations, including changed/unavailable" and the six-leg scope.
2. **Row 1 verdict 2.** `python3 tools/pin-disposition.py --manifest /nonexistent.json --root /home/vgpnk/Projects/shokunin` → exit 2 with `"status": "invalid_input"`, `"kind": "invalid_manifest"` and an emitted JSON error document; matches "2 invalid input/could-not-evaluate".
3. **Row 1 selftest exit 1 on failure.** Source at C* returns 1 on `SELFTEST: FAIL` (`tools/pin-disposition.py` :1321–1328) and 2 on `COULD_NOT_EVALUATE` (:1316–1318); `--selftest` observed `SELFTEST: PASS (19/19)` exit 0.
4. **Row 1 pinned values.** `.ufo/evidence/round-13/pin-manifest.json` exists at C* (sha256 `64eaa43e3f7a928472efa32c7230ca78358235716db04947a93edb0202920af6`, equal to the manifest pin in `.ufo/evidence/round-13/expected.json`); the six-leg mapping and `SELFTEST_CASE …` labels are literals in the tool; the probe validated the manifest against the embedded `tools/mutate-and-run.sh` table and exited 0.
5. **Row 1 write scope.** Normal mode writes nothing (`open(..., "w"/"wb")` appears only inside selftest fixture code at :723, :891, :926); selftest fixtures are created with `tempfile.mkdtemp(…, dir=tempfile.gettempdir())`, i.e. temp-only and TMPDIR-respecting (the row's wording "selftest isolated temp repos only" does not name `/tmp`, so it is unaffected by this round's C2 TMPDIR move).
6. **Row 2 entry command (gate).** `python3 tools/witness-metadata.py --check --companion .ufo/evidence/round-13/witness-metadata.json` → exit 0, `WITNESS_METADATA: metadata_consistent reason=ok … inputs=summary,declaration,declared,rerun_summary`; matches "0 metadata_consistent/clean".
7. **Row 2 verdict 1.** Same command on `.ufo/evidence/round-13/witness-metadata-old-null.json` → exit 1, `metadata_inconsistent reason=normalized_kind_null`.
8. **Row 2 verdict 2 and "including usage".** Every `_fail(..., 2, …)` path maps to `input_unavailable` or `snapshot_tampered` (`tools/witness-metadata.py` :259–268, :293–443); argparse usage errors exit 2.
9. **Row 2 selftest.** `python3 tools/witness-metadata.py --selftest` → `SELFTEST: PASS 39/39`, exit 0; selftest scratch is one `tempfile.mkdtemp()` tree removed in a finally block, so "selftest isolated temp trees only" holds.
10. **Row 2 pinned tool literals.** `PINNED_INPUTS` (summary, declaration, declared), `RERUN_SUMMARY_SHA256`, `EXPECTED_KIND`, `EXPECTED_DISCLOSURE`/`EXPECTED_DISCLOSURE_SHA256` are literals in the tool and the frozen round-12 bytes still match them (the gate's own exit 0 proves the digests). "companion expected verdict" holds: the gate compares the companion's `expected` record to `EXPECTED_VERDICT_ID/EXIT` (:412–418).
11. **Historical producer SHA prose.** "The historical summary's producer SHA names the producer that actually ran, not the repaired current producer": `.ufo/evidence/round-12/BashWitness/summary.json` records `tool.sha256 = 249d9dcd2dfb410f7e6847989da2cb3ab6ef7dd693b87ec2b9b4d6b193d43f1a`; `git -C …/tameshi-shokunin show 546b371a48a2f6bd1e7dca6ae8aee2a6dc1b0a50:tools/bash-witness-study.py | sha256sum` = the same digest (baseline producer bytes), while the repaired producer `producer-oracle.py` is `d5ae0bd4…` and the producer at C* is `cca77724c47619d73902458067aaa9dae8b8f6ea9d4a3ae8507390a3dc8ae85d`. So the sentence holds: it names the baseline version, not the repaired one.
12. **"No old evidence hash is regenerated."** The round-12 summary, declaration and declared digests still equal their pins (`acc01268…`, `e8d2024a…`, `0def0d3b…`), which is what the witness gate's exit 0 verifies; the frozen round-12 bytes are unchanged at C*.
13. **PIT clarification.** `corpus/SOURCES.md:57` (S048) reads "supersedes S047 — item 4 is prioritisation rather than a reuse skip; no claim here resolves its pronoun to test versus mutation"; `corpus/knowledge/incremental-pin-disposition.md:346–349` repeats "S048 supersedes S047's object-specific … a reuse skip; no pronoun referent is resolved here." The paragraph's two sentences match those bytes.

## Finding (1)

Quote (verbatim from the section, byte-exact, single occurrence):

> companion expected verdict; `.ufo/evidence/round-13/expected.json`

Class: dead pointer / misattributed pinned value.

Statement that fails: the witness-metadata gate's pinned values include `.ufo/evidence/round-13/expected.json`.

Why it fails at C*:

- The gate never reads that path: `grep -c 'expected\.json' tools/witness-metadata.py` → `0`; its only path literals are `DEFAULT_COMPANION_REL = ".ufo/evidence/round-13/witness-metadata.json"`, the three `PINNED_INPUTS` round-12 files and `RERUN_SUMMARY_REL`.
- Falsifier by removal: a copy of the C* tree with `.ufo/evidence/round-13/expected.json` deleted still runs the documented entry command to exit 0,
  `WITNESS_METADATA: metadata_consistent reason=ok exit=0 companion=…/tree2/.ufo/evidence/round-13/witness-metadata.json inputs=summary,declaration,declared,rerun_summary`.
  A file whose absence cannot change the verdict is not a pinned value of this gate.
- SKILL.md contradicts it at C*: the canonical later row `| witness metadata companion | gate | …` (SKILL.md:2174) lists this gate's pinned values as the companion plus the four frozen round-12 files (`summary.json`, `declaration.json`, `declared.tsv`, `rerun-20261020T035435Z/summary.json`) and omits `.ufo/evidence/round-13/expected.json`.
- Cited as a current pin, the file is also stale: at C* it records `tools/pin-disposition.py` `297253971dab3a558b470a04162b9d768287844dc0e81bf41a1f9f263ff14f11` vs measured `ae4a6763cd5d90087931622d8737797f703c0df16fdf4d2002b68ee0c54bf787`; `tools/bash-witness-study.py` `49e9e5e2…` vs measured `cca77724…`; `tools/mutate-and-run.sh` `75ed934d…` vs measured `977de470…`; and `expected_checks.pin_selftest` expects `SELFTEST: PASS (18/18)` while the tool prints `SELFTEST: PASS (19/19)`. This contradicts the same section's "No old evidence hash is regenerated" if the file is offered as a live pin.
- Bounds of the claim: `.ufo/evidence/round-13/expected.json` is not inert in the lane — `tools/context-capture.py:149` (`EXPECTED_R13_REL`) and `tools/evidence-disposition.py:1900` name it — but neither is the witness-metadata gate, so the registry cell attributes the pin to the wrong consumer.

No other statement in the section failed: the two entry commands, both verdict maps, both selftest commands, the six-leg manifest pin, the write-scope cells, the producer-SHA sentence, the "no regeneration" sentence and the S048/S047 clarification all held under the commands above.

## Scratch and tooling

- All work ran under `/fast/scratch/hyaku/tameshi-r53/w1/T53W1Read13/` (tree export, `TMPDIR`, fixtures); the directory was removed before yielding.
- No tool was installed or upgraded; no pacman transaction was attempted; no git/jj mutating command was run (only `git show`, `git log`, `git ls-tree`, `git archive`, `git rev-parse`, `git cat-file`, `git diff`).
- Deliverables written only to `.ufo/waves/round-53/w1/T53W1Read13.json` and `.ufo/waves/round-53/w1/T53W1Read13.md`.
