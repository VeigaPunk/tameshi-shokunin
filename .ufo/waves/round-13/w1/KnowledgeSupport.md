# KnowledgeSupport — round 13 w1 (read-only review of S003/S041 support)

Status: **not reviewable yet.** `corpus/knowledge/incremental-pin-disposition.md` does not exist at my last check (glob, 2026-10-20). Neither does `tools/pin-disposition.py` or `.ufo/evidence/round-13/pin-manifest.json`. The only round-13 evidence present is `before.json`, `measure.py`, `claims.json`. The findings below are a source-side brief the knowledge entry must meet. I have not reviewed any text of the entry.

Owner: the registry lists `IncrementalKnowledge` (TameshiR13.IncrementalKnowledge) as running. The dispatch file names the same target as `MetadataRepair`. Findings were sent to `TameshiR13.IncrementalKnowledge`. Forward them if the owner is `MetadataRepair`.

## 1. Source reopens (2026-10-20, read-only)

Both URLs were fetched through the reader and are consistent with the registry quotes. I did not compute a raw-body sha256, so the registry hashes (S003 `9054e311…`, S041 `e9cbc3e1…`, from 2026-10-19) are not re-verified.

- **S003** https://stryker-mutator.io/docs/stryker-js/incremental/ (StrykerJS, Docusaurus "current", no version pinned)
  - §Incremental mode: "Reuse is possible when: A mutant was 'Killed'; the culprit test still exists, and it didn't change. A mutant was not 'Killed'; no new test covers it, and no tests changed."
  - §Incremental mode: "**Note**: The dry run remains required; as it discovers tests, mutation coverage per test, and ensures Stryker runs successfully when no mutant is active."
  - §Limitations: "Stryker will not detect any changes you've made in files other than mutated files and test files."
  - §Limitations: "Any other changes to your environment are not detected, such as updates to other files, updated (dev) dependencies, changes to environment variables, changes to `.snap` files, readme files, etc."
  - §Limitations table: test-change detection depends on the runner plugin. The Command runner row reads "Nothing". The detection rules are plugin-dependent.
  - §Forcing reruns: `--force` "rerun[s] all mutants in scope, regardless of the incremental file."
- **S041** https://pitest.org/quickstart/incremental_analysis/ (PIT; the page says "PIT contains an experimental feature"; version not stated)
  - Items 1–3: reuse rules. Item 2: "If a mutation was killed in the last run and neither the class under test or the killing test has changed, then it can be assumed that this mutation is still killed."
  - Item 4: "(since 1.14.4)". It is a prioritisation rule, not a reuse skip.
  - Item 5: "(not yet implemented)".
  - "With the exception of 4), all these optimisations introduce a degree of potential error into the analysis."
  - "class behaviour is defined not only by its bytecode, but also by its dependencies"
  - "Although this assumption seems reasonable, it is currently **unproven**."

## 2. Findings against the claims the entry is expected to make

**F-1 (defect risk, high): "pin match does not establish safe reuse" has no direct source.** S003 never discusses pins or content hashes. Its reuse rule allows reuse when mutated and test files are unchanged, which is the same condition a content pin tests. S003's stated blind spot is environment change ("Any other changes to your environment are not detected"). The sound statement is: identical tracked content does not cover the undetected environment inputs. That is an inference bridge and must be labelled `[INFERENCE]` or cite the blind-spot quote exactly (QUALITY criterion 3).

**F-2 (scope, high): S041 support should quote the dependency paragraph, not only the "potential error" line.** The "potential error" sentence is general. It does not say that a pinned class can still change verdict through dependencies. The dependency paragraph does, and it is the one anchor that bears on "identical content ≠ safe reuse". The entry should quote it and carry "currently unproven" with it. Presenting the rarity assumption as established would be an overclaim.

**F-3 (registry accuracy, medium): S041 row teaches "all but one of its reuse optimisations introduce potential error".** Item 4 is a prioritisation, not a reuse. Item 5 is listed but not implemented. Accurate: items 1–3 are reuse rules that "introduce a degree of potential error"; item 4 is excepted as a prioritisation; item 5 is unimplemented. The row also omits that PIT calls the feature experimental. Any SOURCES correction is a mutable-cell change for main, recorded as an append-only note (QUALITY criterion 4).

**F-4 (unsupported, high if present): "six-leg disposition differs from fresh re-sweep" has no S003/S041 support.** S003 `--force` describes a rerun, not a comparison against tameshi's legs. The leg-level claim must cite tameshi's own evidence (S031 `tools/mutate-and-run.sh:84-89`, and the round-13 pin manifest once it lands). It must not cite S003 or S041.

**F-5 (scope, medium): generalisation.** S003 is StrykerJS only and S041 is PIT (experimental). The entry should not state the F7 method as general. PROVINCE.md:16-17 admits a pattern as general only with evidence from two independent lanes. Two tool docs are not two lanes. Keep it as "two tools document that reuse is conditional".

**F-6 (test-runner scope, medium): detection depends on the runner.** S003's §Limitations table says test-change detection depends on the runner plugin, and the Command runner gets "Nothing". The entry must not assume tests are tracked for any leg whose runner is a command. It also must not treat `mutated + test` content as covering config, fixtures, or the gate script. S003 says those are outside detection ("files other than mutated files and test files").

**F-7 (admission, high): source rows are not yet eligible for Core.**
- S003 and S041 are `queued` in `corpus/SOURCES.md:14` and `:50`. PROVINCE.md:41-42 requires a `mined` row for ground to move to Core.
- QUALITY criterion 10 requires a row "opened in the round that writes it". Both rows were opened 2026-10-19 (kaika round 1). A round-13 search-log entry is needed, as round 12 did at `corpus/SOURCES.md` search log lines 101–111. No such entry exists yet.
- The entry header must follow the existing `knowledge/` convention (`repeated-control-precondition.md:1-3`): `source:` with URL and access date, `verified-at:`, and a `recheck:` no longer than 90d (S041's cadence, the shorter of the two).

**F-8 (coverage map, medium): QUALITY criterion 7.** A new knowledge file needs its coverage-map row in the same round. The F7 row at `corpus/README.md:84` still reads "pin-level cadence only → per-leg reuse decisions classified" and "open". It must name the new file, or the missing row must be logged as owned debt in LOG.md. Main owns this integration.

**F-9 (what is correctly supported, no action): the basic reuse-with-error claim.** S041's "potential error" sentence and S003's "dry run remains required" are accurate quotes of the sources. An entry that cites only these two as the "reuse is conditional, verify" point is supported.

## 3. Exact checks for L1 to run (not executed by me)

1. Source drift: `curl -fsSL https://stryker-mutator.io/docs/stryker-js/incremental/ | sha256sum` and compare with `9054e311a0569231aa2a1427a4137729c8180d7f2687dfd450322e855cc9ad90`. Same for `https://pitest.org/quickstart/incremental_analysis/` against `e9cbc3e1a…590db`. A mismatch means re-quote, not a silent update.
2. Quote anchors, run after the entry lands:
   - `curl -fsSL <S003 url> | grep -c 'Any other changes to your environment are not detected'` → expect 1.
   - `curl -fsSL <S041 url> | grep -c 'class behaviour is defined not only by its bytecode'` → expect 1.
   - `curl -fsSL <S041 url> | grep -c 'it is currently'` → expect 1.
3. `grep -n 'pin' corpus/knowledge/incremental-pin-disposition.md` and check each pin/match/reuse sentence either cites S003/S041 with a quote or carries `[INFERENCE]`.
4. `grep -n 'S003\|S041' corpus/knowledge/incremental-pin-disposition.md` and confirm no S003/S041 citation supports a six-leg or tameshi-specific claim.
5. `grep -n 'round-13' corpus/SOURCES.md` → expect a round-13 search-log entry for the S003/S041 re-open.
6. `grep -n '^| F7' corpus/README.md` → expect the new knowledge file named, or a LOG.md debt entry.
7. `grep -n 'incremental-pin-disposition' corpus/**` → confirm the entry is referenced from the mutable coverage row; the knowledge entry header carries `source:`, `verified-at:`, `recheck:`.

## 4. Not done

- I did not edit any implementation file, the knowledge file, or the SOURCES registry.
- I did not run tests, builds, or lint.
- I did not compute raw sha256 values; I relied on the reader and the registry hashes.
- I did not open any sibling gate code.

## 5. Tooling record

No tools installed or updated. I used only the `read`, `glob`, `grep`, and `write` tools.

## 6. Text review of the landed entry (2026-10-20, read-only, no tests)

Reviewed `corpus/knowledge/incremental-pin-disposition.md` as written, `corpus/SOURCES.md` S003/S041/S047 rows, and `corpus/lessons/round-13.md`. Supersedes the pre-landing status in §§1–5 above.

Verified as correct: S003 re-fetch 33,898 B / sha `9054e311…`; S041 8,892 B / sha `e9cbc3e1…`, both matching the header and `.ufo/evidence/kaika-round-1/sources-opened.tsv:4,:33`. The four recheck greps each return 1. Leg pins, revs and expectations match `tools/mutate-and-run.sh:84-89` and `:542-553`. Runner anchors `:99-108`, `:104-106`, `:109-114` (quote at 110-112), `:119-120`, `:959`, `:1113-1140` match. Sibling anchors match: surface-census `:82-83`, `:710`, `:789-790`, `:817-823`; checklist-run `:65`, `:68`, `:416`, `:438-439`; claims-check `:82-93`, `:582-583`, `:600`; `mutation-case-kagi-census.md:27-30`; ER-4 LEDGER line; round-10 `:84-88`; kagi SKILL.md +4/−2.

Defects (sent to IncrementalKnowledge):

1. Knowledge §7 (lines 284-290): "SOURCES rows record no digest from their opening fetch … byte identity … unestablished" is false. `sources-opened.tsv:4,:33` record the same digests at 2026-10-19; the 2026-10-20 fetch matches. Correct to established identity.
2. Knowledge §1 line 61, `SOURCES.md:56`, `lessons/round-13.md:12`: "item 4 prioritises an old killing test" / "prioritises tests". Source: "it should therefore be prioritised above others", where "it" is the mutation. Knowledge lines 57-58 are already correct.
3. Knowledge §2 lines 81-83 and §1 line 47: "(for PIT) the class have not changed" and "conditional on the class and the killing/covering tests". Item 3 conditions only on covering tests. Item 2 is class OR killing test. Item 1 is class.
4. Knowledge §1 lines 38-40: "`--force` exists because the detection is incomplete" is not on the page. The page says "With these limitations in mind, you can probably imagine a scenario where you want to force specific mutants to run". Quote it or mark [I].
5. Knowledge §1 line 18: "quoted verbatim" with double quotes; the page uses single quotes for 'Killed'. Note the normalization.
6. Knowledge §3 line 138 and §5a lines 218-220: "identical bytes" for the round-10 SETUP. `plans/round-10-record-draft.md:84-88` says only that the materialized blob lacked the exec bit. Label [I] or drop.
7. Knowledge §5a lines 211-212: "Same bytes, different PATH ⇒ a different executed case set" is a deduction from `:817`, under the "(O, read-only)" heading. Label [I].
8. Knowledge §4 line 171: "a re-sweep is not required by a current reading" is an inference; `fleet-kill-rate-ledger.md:293` says only "a re-sweep is a fresh reading, not a repair". Label [I].
9. Knowledge §4 line 167: the trigger list includes "owner hardening"; trigger 1 was not visible in my read (ledger lines 309-310 show triggers 2 and 3). Cite its line or drop it.
10. `lessons/round-13.md:40`: "S041 calls all but one item a reuse optimisation". The page says "all these optimisations"; "reuse" comes from the registry row.

No item above is a test or build result. Checks L1 may run, not run by me: re-hash both URLs against the header digests; `grep -n 'prioritised above others' corpus/knowledge/incremental-pin-disposition.md`; `grep -n 'no digest from their opening fetch' corpus/knowledge/incremental-pin-disposition.md` (expect 0 after fix).
