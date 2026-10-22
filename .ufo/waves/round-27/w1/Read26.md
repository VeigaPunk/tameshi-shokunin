# Read26 cold read: Pin disposition and provenance correction — round 13

**Verdict: gap-minor** (class `instruction`). Section: SKILL.md lines 1517–1547 at 2227d8338c02aa9a5fd7d95c1a41b76865ad7647. Heading at line 1517; the next heading is `### Round-13 gate/probe registry` at line 1548. Page sha256 386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95 (matches).

No blocking gap and no wrong expectation. Every claim I could check held on the pinned clone. Seven minor gaps are listed below, each with its smallest correction. One execution gap is mine, not the section's: step 2 ran against a copy mirror, not the literal fleet-root path.

## Evidence

Setup. Step-1 fleet mirror at /tmp/Read26-VwbA/fleet, a detached clone of the lane at 2227d83. The step-1 sibling symlinks broke step 2 (E1), so I rebuilt the four leg repos (kumitate-shokunin, kagi-shokunin, tsukuroi-shokunin, mado-shokunin) as real directories: a copy of each `.git` plus byte-identical copies of the six leg files. Those copies match the live files (E7). Writes: trace receipts under `.ufo/evidence/round-27/coldread/traces/` and this report only.

E1. Step 2 on the step-1 mirror, traced (Read26-1), argv `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /tmp/Read26-VwbA/fleet`. Exit 0. Counts: unchanged 0, changed 0, unavailable 6. Every pinned, head and worktree field is `unavailable` with reason `repo_symlink` (`tools/pin-disposition.py:259`). observed_at 2026-10-22T12:47:12Z. [O]

E2. Step 2 on the copy mirror, traced (Read26-4), same argv. Exit 0; status ok; observed_at 2026-10-22T12:48:58Z; counts legs 6, unchanged 1, changed 5, unavailable 0. `result_reuse` is `not_established` on all six rows. `not_compared` lists the eight items at `tools/pin-disposition.py:125-134`. [O]

| leg | pinned blob equals expected pin | branch tip (master) commit | branch-tip blob | worktree | content_status |
|---|---|---|---|---|---|
| js-kimi-census | verified | f69817edf6 | 7818970b80d4 | changed | changed |
| bash-surface-census | verified | 899c50b426 | 1e697b017954 | changed | changed |
| bash-tsukuroi-census | verified | e9f5356cd6 | d17d32a35946 | changed | changed |
| bash-mado-verify | verified | 8e5d93691e | 050efc720599 | changed | changed |
| bash-checklist-run | verified | 899c50b426 | 7e5ec98b9e1d | unchanged | unchanged |
| js-claims-check | verified | f69817edf6 | 0b2d0d24e4ee | changed | changed |

In all six rows the worktree bytes equal the branch-tip blob at copy time, so the pins differ because the sibling files moved on, not because the copies diverge.

E3. Step 3, traced (Read26-2): `WITNESS_METADATA: metadata_consistent reason=ok exit=0 ... inputs=summary,declaration,declared,rerun_summary`. Exit 0. [O]

E4. Frozen round-12 bytes (hashes in Read26-8; fields in Read26-3). summary.json acc01268…, declaration.json e8d20248…, declared.tsv 0def0d3b…, rerun summary 6726421f…. These equal the digests pinned in `tools/witness-metadata.py` (PINNED_INPUTS). `summary.declaration.kind` is null, and so is the rerun's. `declaration.json` top-level `kind` is "declared-witness mapping (not a blind preregistration)". The summary's disclosure equals the declaration's disclosure, with sha256 ec6e5be7…, which is the companion's `disclosure_sha256`. `summary.tool.sha256` is 249d9dcd…, the historical producer that the companion pins. [O]

E5. Producer. `tools/bash-witness-study.py` (sha256 60575e62…, not 249d9dcd…) reads the top-level declaration at line 797 (`"kind": declaration.get("kind"),`). No nested declared-kind read remains. Its selftest asserts the top-level exposed kind at line 1681. `python3 tools/bash-witness-study.py selftest`, traced (Read26-5): `WITNESS_SELFTEST: 51/51 pass`, `VERDICT: PASS`, exit 0. This is the lane's own producer selftest, run in the clone; it is not a sibling gate. [O]

E6. Sources and cited files (Read26-3, plus hand reads). `corpus/SOURCES.md`: S003 row line 14; S041 row line 50 (old text kept); S047 row line 56 ("precision correction"); S048 row line 57 ("supersedes S047"). `corpus/lessons/round-12-verifier-spotcheck.md:146` is "Routed defects" item 3 and names the nested `declaration.kind=null` defect. `corpus/knowledge/incremental-pin-disposition.md` line 1 names S003, S041 and S047; line 5 names S048 as the source correction. Receipt Read26-6 records 18 dropped /home opens (git reading user config); none were hashed. [O]

E7. Pins and copies. `pin-manifest.json` expected_sha256 and pinned_commit equal the PIN_* and REV_* constants in `tools/mutate-and-run.sh` lines 603–614 for all six legs (Read26-3). The pinned blobs at the pinned commits hash to the expected values (Read26-6). The live leg files hash to the same bytes as the copy mirror's worktree rows (Read26-7 against E2). [O]

E8. Table rows, by evidence.
- Row 1 (`unchanged`): bash-checklist-run in E2.
- Row 2 (`changed`): five legs in E2.
- Row 3 (`unavailable`, with reason): `repo_symlink` (E1). `repo_missing` and `repo_foreign` (Read26-9): a stub fleet root that is a git repo, holding a plain `kagi-shokunin/` directory and no other leg repos. The kagi legs read `repo_foreign`, so nothing was borrowed from the stub HEAD and nothing was labelled unchanged; the other four legs read `repo_missing`. `pinned_commit_missing` (Read26-10 and Read26-11): a scratch manifest pins leg one to 40 zeros. That leg's pinned status is unavailable with `pinned_commit_missing`, its worktree is unavailable with `pin_not_verified`, and its content_status is unavailable. The other five legs still evaluate.
- Row 4 (`result_reuse=not_established`): every row in E2. The all-three-agree case is bash-checklist-run only.
- Row 5 (frozen null, explicit top level, companion): E3 and E4.
- The probe's own selftest, traced (Read26-12): `SELFTEST: PASS (19/19)`, no FAIL lines. Its cases include repo-symlink, worktree-symlink and worktree-outside-repo. [O]

E9. Retained round-13 receipt, hand read only: `.ufo/evidence/round-13/pin-dispositions.json`. Tool `pin-disposition.py r13 (tameshi-shokunin, 2026-10-20)`; observed_at 2026-10-20T04:59:26Z; counts unchanged 3, changed 3, unavailable 0; root /home/vgpnk/Projects/shokunin (the literal fleet root). Against the 2026-10-22 reading it differs on bash-surface-census and js-claims-check, both unchanged then and both changed now. [INFERENCE] Both sibling files have later mtimes on this host (Oct 21 00:56 and Oct 21 03:37, after the receipt time), so the difference reads as sibling drift, not a probe fault.

## Minor gaps and smallest corrections

These seven entries match the JSON `minor_gaps` array.

1. Sources line (1519–1520) omits S048, which supersedes S047's object-specific paraphrase. Correction: add S048.
2. Step 2 (1535) needs one precondition sentence: each leg repo must be a real directory. Symlinked repos give six `repo_symlink` rows (E1).
3. Step 2 (1536) says "retain stdout" but names no destination. The retained receipt came from the r13 tool, not the r17 tool at this revision (`tools/pin-disposition.py` line 109). Correction: name the receipt path and the tool revision that writes it.
4. Row 1 Limit cell (1526) lists five of the probe's eight NOT_COMPARED items and uses "invocation identity", a phrase the probe does not use (`tools/pin-disposition.py:125-134` say "suite command and test harness"). Correction: point the cell at the probe's list.
5. Row 4 (1529) says "all three content identities" without defining them. The probe supplies the expected pin, the pinned-commit blob, the branch-tip blob and the worktree sha256. In E2 only bash-checklist-run has the expected pin, branch-tip blob and worktree all equal. Correction: define the three in one clause.
6. Step 5 (1545–1546) asks a closure reader to verify "their measured revision", but neither the probe JSON nor the round-13 companion records a lane revision. Only a trace receipt's `rev` carries one. Correction: name the revision source.
7. Execution gap of this cold read, not a section defect. Step 2 ran against a copy mirror, not the literal `--root /home/vgpnk/Projects/shokunin`, because this seat must not read the live fleet root. Step 3 ran exactly as written.

## Residual risk and verification gaps

- Dated reading. The 2026-10-22 numbers are a snapshot of the copies taken around 12:48Z. Sibling heads may have moved since, and I did not re-read after copying.
- Not run at the literal live root. I checked real directories only for the four leg repos (their `.git` directories and leg files), not the whole live fleet.
- Mode (exec-bit) is not tested. The probe docstring says a chmod-only change stays unchanged and is unmeasured (`tools/pin-disposition.py:60-65`). I did not test it.
- Not cited and not opened: `.ufo/evidence/round-17/coldread/assemble.py` and `measure.py` (named in the monitor drift list); `witness-metadata.py --selftest`.
- Provenance pointers (not a claim of the section, but step 2 consumes this manifest). `pin-manifest.json` names `derived_from` sha256 75ed934d… and line ranges :84–89, :542–553 and :1112–1140. Those point at the runner before the round-16 move (SKILL.md:1581–1582). At 2227d83 the runner is fb91ef76…, and the same six pin/revision pairs sit at lines 603–614. The values agree 6 of 6; the stale pointers are not disclosed. Smallest correction: an append-only pointer update, outside this seat's bounds.
- Receipts record only opens under the root. Sibling git-object reads and /tmp copies appear in no receipt, so they are carried in `external_inputs`: pinned blobs as `repo@rev:path`, live worktree files as absolute paths.

## Untraced commands and disclosures

- Setup and listings: `mktemp`, `mkdir`, `ln -s` for the step-1 mirror; `git clone --no-hardlinks` from the lane (read only); `git checkout --detach 2227d83…`; `git rev-parse HEAD`; `sha256sum` of SKILL.md (386de44b…). SKILL.md is deliberately not traced, so it cannot enter any receipt's input map. `ls` and `du` metadata listings of sibling repos, of the fleet-root directory (a `cd` into it, with no git call there), and of two lane directories. `unlink` of four mirror symlinks (the link only).
- Copies: `cp -a` of four sibling `.git` directories and `cp -p` of six leg files, read only.
- Scratch: `git init` and one commit in /tmp/Read26-VwbA/borrow-test; `python3 -c` reads of receipts and probe output; a formatting script that re-hashed every input in the clone, checked the copy against the live bytes, and wrote nothing into the lane.
- Before the traced hashing (Read26-8 and Read26-13), I hashed files with `git show | sha256sum` in the clone. Those hashes match the traced ones.
- Hand reads through the read and grep tools are listed in `opened`.
- No tools installed or upgraded.

```json
{
  "schema": "tameshi-coldread-report-v2",
  "seat": "Read26",
  "skill_sha256": "386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95",
  "read_rev": "2227d8338c02aa9a5fd7d95c1a41b76865ad7647",
  "sections": [
    {
      "start": 1517,
      "heading": "## Pin disposition and provenance correction — round 13",
      "class": "instruction",
      "verdict": "gap-minor",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [
        "Sources line (lines 1519-1520) omits S048. S048 supersedes the object-specific paraphrase in S047 (corpus/SOURCES.md rows S047 and S048; corpus/knowledge/incremental-pin-disposition.md line 5). S047 remains the precision-correction row, so this is a citation-currency gap. Smallest correction: add S048 to the Sources line.",
        "Recipe step 2 (line 1535) has an unstated precondition: every leg repo must be a real directory. With symlinked sibling repos the probe reports all six rows unavailable with reason repo_symlink (receipt Read26-1; observed_at 2026-10-22T12:47:12Z). Smallest correction: add one sentence naming this precondition.",
        "Recipe step 2 says to retain stdout (line 1536) but names no destination. The retained receipt .ufo/evidence/round-13/pin-dispositions.json was written by pin-disposition.py r13 (tool_sha256 297253971dab...), not by the r17 tool at this revision (tool_sha256 331529eadafe...; tools/pin-disposition.py line 109). Smallest correction: name the receipt path and the tool revision that writes it.",
        "Table row 1 Limit cell (line 1526) lists five of the probe's eight NOT_COMPARED items and uses the phrase invocation identity, which the probe does not use (tools/pin-disposition.py lines 125-134 say suite command and test harness). The statement is true as far as it goes. Smallest correction: point the cell at the probe's NOT_COMPARED list.",
        "Table row 4 (line 1529) uses all three content identities without defining them. Per leg the probe supplies the expected pin, the blob at the pinned commit, the branch-tip blob and the worktree sha256. The bash-checklist-run leg (7e5ec98b...) is the only leg in the 2026-10-22 run where the expected pin, the branch-tip blob and the worktree all agree. Smallest correction: define the three identities in one clause.",
        "Step 5 (lines 1545-1546) asks a closure reader to verify their measured revision. Neither the probe JSON (keys counts, legs, manifest, not_compared, observed_at, result_reuse, result_reuse_reason, root, schema, status, tool, tool_sha256) nor the round-13 companion records a lane revision; only a trace receipt's rev carries one. Smallest correction: name the revision source.",
        "Execution gap of this cold read, not a section defect. Step 2 was not run with its literal --root /home/vgpnk/Projects/shokunin, because this seat must not read the live fleet root. It was run against a copy mirror in which the four leg repos are real directories with copied .git directories and byte-identical copies of the six leg files (live bytes matched at receipt Read26-7). Step 3 ran exactly as written."
      ],
      "commands_executed": [
        "python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /tmp/Read26-VwbA/fleet",
        "python3 tools/witness-metadata.py --check --companion .ufo/evidence/round-13/witness-metadata.json",
        "python3 /tmp/Read26-VwbA/record_check.py",
        "python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /tmp/Read26-VwbA/fleet",
        "python3 tools/bash-witness-study.py selftest",
        "bash /tmp/Read26-VwbA/pinned_blobs.sh",
        "sha256sum /home/vgpnk/Projects/shokunin/kumitate-shokunin/scripts/kimi-census.mjs /home/vgpnk/Projects/shokunin/kagi-shokunin/corpus/surface-census.sh /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh /home/vgpnk/Projects/shokunin/kagi-shokunin/corpus/checklist-run.sh /home/vgpnk/Projects/shokunin/kumitate-shokunin/scripts/claims-check.mjs",
        "sha256sum tools/trace-inputs.py tools/pin-disposition.py tools/witness-metadata.py tools/bash-witness-study.py tools/mutate-and-run.sh .ufo/waves/round-26/w1/ColdreadPilot.md corpus/SOURCES.md corpus/knowledge/incremental-pin-disposition.md corpus/lessons/round-12-verifier-spotcheck.md .ufo/evidence/round-13/pin-manifest.json .ufo/evidence/round-13/witness-metadata.json .ufo/evidence/round-12/BashWitness/summary.json .ufo/evidence/round-12/BashWitness/declaration.json .ufo/evidence/round-12/BashWitness/declared.tsv .ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json",
        "python3 /tmp/Read26-VwbA/fleet/tameshi-shokunin/tools/pin-disposition.py --manifest /tmp/Read26-VwbA/fleet/tameshi-shokunin/.ufo/evidence/round-13/pin-manifest.json --root /tmp/Read26-VwbA/borrow-test",
        "python3 /tmp/Read26-VwbA/mk_missing_commit.py",
        "python3 tools/pin-disposition.py --manifest /tmp/Read26-VwbA/manifest-missing-commit.json --root /tmp/Read26-VwbA/fleet",
        "python3 tools/pin-disposition.py --selftest",
        "sha256sum .ufo/evidence/round-13/pin-dispositions.json corpus/knowledge/incremental-pin-disposition.md"
      ],
      "opened": [
        "tools/trace-inputs.py",
        "tools/pin-disposition.py",
        "tools/witness-metadata.py",
        "tools/bash-witness-study.py",
        "tools/mutate-and-run.sh",
        ".ufo/waves/round-26/w1/ColdreadPilot.md",
        "corpus/SOURCES.md",
        "corpus/knowledge/incremental-pin-disposition.md",
        "corpus/lessons/round-12-verifier-spotcheck.md",
        ".ufo/evidence/round-13/pin-manifest.json",
        ".ufo/evidence/round-13/witness-metadata.json",
        ".ufo/evidence/round-13/pin-dispositions.json"
      ],
      "inputs": {
        ".ufo/evidence/round-12/BashWitness/declaration.json": "e8d2024ad13e021c5b7c41a66b881225beb9e0b30190833f0ab2310cf3670901",
        ".ufo/evidence/round-12/BashWitness/declared.tsv": "0def0d3b370288f58048c7dfb05aec652f9a262664e9f9ce27ae8fad5e6741d3",
        ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json": "6726421fde88e8d2aff4c9d0ff4a4fdce9b1d4651da50b89f2bf29f65a22a5f0",
        ".ufo/evidence/round-12/BashWitness/summary.json": "acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9",
        ".ufo/evidence/round-13/pin-dispositions.json": "210850f51040fd11d5c63711417f72fb816171a55a23d82f52f7969be711a637",
        ".ufo/evidence/round-13/pin-manifest.json": "64eaa43e3f7a928472efa32c7230ca78358235716db04947a93edb0202920af6",
        ".ufo/evidence/round-13/witness-metadata.json": "463282270a04bd46f4a0522ff6a349b77d268ede47725c4e1c52ca892210bd8d",
        ".ufo/waves/round-26/w1/ColdreadPilot.md": "428a61a30ff8cf9e02f5a2a0923f916cf5f4c98596d2ace022f9d982fc25ceb7",
        "corpus/SOURCES.md": "0a66531dde7f086005ddf131a3bc5f920a15af5b614fccd631f8d5a668a58e5a",
        "corpus/knowledge/incremental-pin-disposition.md": "0cc87300978412e774c8768936dbbac08fe90581da762bfd5a8f20fbd6fcf0b9",
        "corpus/lessons/round-12-verifier-spotcheck.md": "6ec29ffdf3bbe2f5bbcda3405a6e0ba51c2f5d02467c681d7c892edb3feafe30",
        "tools/bash-witness-study.py": "60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9",
        "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de",
        "tools/pin-disposition.py": "331529eadafe9138c88c1fe09666c9401d28c166f16bc92ecc092fc4d92c3a4c",
        "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4",
        "tools/witness-metadata.py": "df3390682a04ccbb2469060c3deab924f9d8df72ce1a5b195d3618ce6cc0bed4"
      },
      "external_inputs": {
        "kumitate-shokunin@175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/kimi-census.mjs": "83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426",
        "kagi-shokunin@fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/surface-census.sh": "275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f",
        "tsukuroi-shokunin@165307fe4746a8807b02ec4a7d7ecac0368454a6:tools/tsukuroi-census.sh": "084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5",
        "mado-shokunin@eead56b20ad2b28299ae4fa623d52a99b44c743c:tools/mado-verify.sh": "d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13",
        "kagi-shokunin@fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/checklist-run.sh": "7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf",
        "kumitate-shokunin@175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/claims-check.mjs": "e9a21b441f1216bf41d1cca037b36021c581ec7892df3bf973295f9321b0f61b",
        "/home/vgpnk/Projects/shokunin/kumitate-shokunin/scripts/kimi-census.mjs": "7818970b80d4951b8edf15dcc8c5a16efe57f457f956a5ce019f049068538156",
        "/home/vgpnk/Projects/shokunin/kagi-shokunin/corpus/surface-census.sh": "1e697b0179547a869b73fcf966ce05dd60b07adbe7094a95d3d0a2d4102de11d",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh": "d17d32a35946c71c1fc195e36178aa383f4a04d7172cc579b6e9e25fa537f27e",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh": "050efc720599345a73bdce6c1d13d50eadeee9769c2ece02462223d0156703f1",
        "/home/vgpnk/Projects/shokunin/kagi-shokunin/corpus/checklist-run.sh": "7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf",
        "/home/vgpnk/Projects/shokunin/kumitate-shokunin/scripts/claims-check.mjs": "0b2d0d24e4ee83c8934a9e9390aeee9105a8e3f9b203997c7a68b7b5b74de487"
      },
      "traces": [
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read26-1.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read26-2.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read26-3.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read26-4.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read26-5.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read26-6.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read26-7.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read26-8.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read26-9.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read26-10.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read26-11.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read26-12.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read26-13.json"
      ]
    }
  ]
}
```

Plain-English note. I checked the section's five-row table against probe runs on real copies of the four leg repos, including the refusal cases: a symlinked repo, a missing repo, a foreign repo and a missing pinned commit. I re-ran the witness check and the producer selftest, and read the frozen round-12 bytes against their pinned digests. I confirmed that the Sources IDs and the routed defect exist, and that the nulls and the top-level kind say what the section says. I did not run step 2 at the literal fleet root; that is my one execution gap. The section's seven gaps are wording and precondition gaps, not false claims.

COLDREAD Read26: gap-minor
