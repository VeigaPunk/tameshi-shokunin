Cold read — Read14 — section "The tick and the pin read" (SKILL.md:1021-1068) at tameshi rev 2227d8338c02aa9a5fd7d95c1a41b76865ad7647.

```json
{"schema": "tameshi-coldread-report-v2", "seat": "Read14", "skill_sha256": "386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95", "read_rev": "2227d8338c02aa9a5fd7d95c1a41b76865ad7647",
  "sections": [{"start": 1021, "heading": "### The tick and the pin read", "class": "record", "verdict": "verified-record",
    "blocking_gaps": [], "wrong_expectations": [],
    "minor_gaps": [
      "Tick scratch is gone: /tmp/w8-tameshi-t84/pin-read.txt and /tmp/w8-tameshi-t84/drift-demo.txt no longer exist on this host, so the tick's timestamp (2026-10-14T19:15:14Z), host (plazir27), and the re-read's transient size/mtime (99,716 B, mtime 16:19:40) rest on the section's own record plus cross-corroboration in corpus/knowledge/fleet-kill-rate-ledger.md:326-338, not re-observation.",
      "tools/mutate-and-run.sh has moved since the tick (fb91ef76… at 2227d83 vs the ticked cf41efaa…, bytes recoverable at lane 9f1d3c33): the tick's tool `held` reading is a 2026-10-14 observation (corroborated by the ledger's r7-1/r8 harness pins at fleet-kill-rate-ledger.md:276-277, :346-348), not a standing claim — consistent with the section's own held/moved semantics and this read's monitor reason input-drift:tools/mutate-and-run.sh.",
      "All four recorded case revisions have since been superseded on refs/heads/master (kumitate tip f69817ed, kagi 899c50b4, tsukuroi e9f5356c, mado 8e5d9369): re-running the readings today marks every recorded row except checklist-run `stale` — exactly the timestamped-observation behavior the section prescribes, not a defect in the recorded table."
    ],
    "commands_executed": [
      "python3 tools/trace-inputs.py --root /tmp/Read14-r4qw/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read14-1.json -- python3 -c \"import sys,hashlib; [print(p, hashlib.sha256(open(p,'rb').read()).hexdigest()) for p in sys.argv[1:]]\" tools/mutate-and-run.sh",
      "python3 tools/trace-inputs.py --root /tmp/Read14-r4qw/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read14-2.json -- python3 -c \"import sys,hashlib,subprocess,os; tip=sys.argv[1]; u,d=sys.argv[2],sys.argv[3]; su=hashlib.sha256(open(u,'rb').read()).hexdigest(); sd=hashlib.sha256(open(d,'rb').read()).hexdigest(); print('untouched copy sha',su,'== tip:',su==tip,'-> reading current' if su==tip else '-> reading NOT-current'); print('appended-line copy sha',sd,'!= tip:',sd!=tip,'-> reading drift' if sd!=tip else '-> reading NOT-drift'); p=subprocess.run(['git','-C','../kagi-shokunin','status','--porcelain','--','corpus/surface-census.sh'],capture_output=True,text=True,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'}); print('substrate porcelain lines after:',len(p.stdout.splitlines()),repr(p.stdout)); sys.exit(0 if (su==tip and sd!=tip and len(p.stdout.splitlines())==0) else 1)\" 1e697b0179547a869b73fcf966ce05dd60b07adbe7094a95d3d0a2d4102de11d /tmp/Read14-scratch/gate-untouched.sh /tmp/Read14-scratch/gate-drift-demo.sh",
      "python3 tools/trace-inputs.py --root /tmp/Read14-r4qw/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read14-3.json -- bash /tmp/Read14-scratch/tool-cf41efaa.sh --selftest --workdir /tmp/Read14-scratch/st-work3"
    ],
    "opened": [
      "tools/mutate-and-run.sh",
      "corpus/knowledge/fleet-kill-rate-ledger.md",
      "corpus/knowledge/incremental-pin-disposition.md",
      "corpus/knowledge/arm-class-matrix.md",
      "corpus/knowledge/closeout-r11.md",
      "corpus/knowledge/executor-test-sufficiency.md",
      "corpus/knowledge/mutation-case-kumitate-claims.md",
      "corpus/knowledge/gates-survey-kagi.md",
      "corpus/knowledge/operator-runbook.md"
    ],
    "inputs": {
      "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de",
      "corpus/knowledge/fleet-kill-rate-ledger.md": "13a11e468dbf26972bb9734c2f0bedec859386f6729225c367c61ba056d7499e",
      "corpus/knowledge/incremental-pin-disposition.md": "0cc87300978412e774c8768936dbbac08fe90581da762bfd5a8f20fbd6fcf0b9",
      "corpus/knowledge/arm-class-matrix.md": "bd4f4a02eb66f4e25e67a1518108d1f11c45b4edf2355d1901ec54ce55359088",
      "corpus/knowledge/closeout-r11.md": "cea3352aa60eb51b51e2722fdb820cac19cd1514670df931212904e826940265",
      "corpus/knowledge/executor-test-sufficiency.md": "b26021292d69b3686851e13363d8451009f12a32dc85925b5a7cd2295e34cf07",
      "corpus/knowledge/mutation-case-kumitate-claims.md": "3da1312e0a624ca565dc243fd0cb6f19968c1672f57066fbd4d2ad2bdf8045d9",
      "corpus/knowledge/gates-survey-kagi.md": "4734f0a0bd28e90f78b0a766b2aa6dac8238936550e1b1b0ec3316b00e1294c6",
      "corpus/knowledge/operator-runbook.md": "8b2e185ff011f6cfc2aee187ff1c2a1f8120e410c00f4b67eb6c7f1ebabb6859"
    },
    "external_inputs": {
      "shokunin@17c1fadfddc5ecbfa5ef362ef44d111792fa3e94:scripts/shokunin-watchdog.sh": "b8b01a78b9f66e343a6d5eefd027622b3c3718f79db2c7c06bb69c047fbe2226",
      "shokunin@5efb4114e8a4f6ff17d0b1594cb0767b144e4f9c:shokunin.conf": "a42e8406082ebb9a4248d91df06cb331c365b94e3ce877a6d8652363baebc5ee",
      "shokunin@1fc0832390cbf839a892ee304ba9d4c2545c9512:scripts/hyaku/jj-lane.sh": "319a56f7f0641915bdb636d88b2d6b34987a20f430d7b06896150f8ae4c1e429",
      "tameshi-shokunin@9f1d3c339a7094968041c7708a65dbf7eab9fae6:tools/mutate-and-run.sh": "cf41efaa8be5f52d92bf7806ddb3a99a031547bf12a6811b8ef45bce37242c75",
      "kumitate-shokunin@175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/kimi-census.mjs": "83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426",
      "kumitate-shokunin@175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/claims-check.mjs": "e9a21b441f1216bf41d1cca037b36021c581ec7892df3bf973295f9321b0f61b",
      "kagi-shokunin@fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/surface-census.sh": "275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f",
      "kagi-shokunin@fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/checklist-run.sh": "7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf",
      "tsukuroi-shokunin@165307fe4746a8807b02ec4a7d7ecac0368454a6:tools/tsukuroi-census.sh": "084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5",
      "tsukuroi-shokunin@aa136d69e0e4666b86782152cd1d1fa00f90a0b3:tools/tsukuroi-census.sh": "bba6cdf6f5b7a7372e43230821bb7c12aa64192266c549f39475c948803a4f55",
      "mado-shokunin@eead56b20ad2b28299ae4fa623d52a99b44c743c:tools/mado-verify.sh": "d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13",
      "mado-shokunin@0c20a76fa5ff985047c8ca2d455c75179c3dd0d1:tools/mado-verify.sh": "90d50cdd4d18410bd1e4222e12f566986c5d8d8cfdffd6f86864a3de5a3100bd",
      "/home/vgpnk/Projects/shokunin/kagi-shokunin/.gitignore": "3767312444cc6425c133ea7e335892948272aa886559e4cc3d3e41a5394ce74e"
    },
    "traces": [
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read14-1.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read14-2.json",
      "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read14-3.json"
    ]}]}
```

What I checked, against the clone at 2227d83 (fleet-mirror, detached; SKILL.md sha256 matches the assignment):

- **Tick idiom (fleet `17c1fad`).** `git show 17c1fad…:scripts/shokunin-watchdog.sh` lines 3-5 say a lane's round ends when `.ufo/reports/round-<N>/<lane>.md` lands, and "Tick 450s" (also `INTERVAL=450` at line 10); line 14 is exactly the `LANES="protocol aggregator kasegi kengaku kake kumitate kotoba kagi kama"` map — no tameshi. Both line anchors in the section are correct. `5efb4114` (2026-10-19) is the commit "substrate-neutral launch from shokunin.conf LANES" (watchdog-only diff), and `shokunin.conf` at that commit names tameshi at line 55. All three claims check.
- **Branch helper.** Live `scripts/hyaku/jj-lane.sh` (worktree bytes == fleet HEAD blob, sha256 319a56f7…): `state` prints a `branch=` field (line 182), resolves it git-config `lane.branch` first (lines 103-105, 165) then `detect_branch()` (line 118). Matches the section's parenthetical.
- **The tick table.** All six recorded pins re-derive exactly from the sibling repos: `git show 175de6ba…:scripts/kimi-census.mjs` = 83016d45…, `175de6ba…:scripts/claims-check.mjs` = e9a21b44…, `fecee874…:corpus/surface-census.sh` = 275d8294…, `fecee874…:corpus/checklist-run.sh` = 7e5ec98b…, `165307fe…:tools/tsukuroi-census.sh` = 084951be…, `eead56b2…:tools/mado-verify.sh` = d7edaab4…. The tick-time live blobs also re-derive: tsukuroi @ aa136d69 → bba6cdf6 (row 3, `stale`), mado @ 0c20a76f → 90d50cdd (row 4, `stale`); kagi/kumitate tips at the tick were the recorded revs (rows 5-6 `HEAD (r8)` = fecee874/175de6ba per fleet-kill-rate-ledger.md:330-331). 4 × current · 2 × stale arithmetic is internally consistent, and the ledger's pin-read rows (:326-331) plus incremental-pin-disposition.md:159-161 record the same rev/pin pairs.
- **Tool `held`.** The ticked harness bytes exist in lane history at 9f1d3c33 and hash to cf41efaa8be5…, matching the section's `cf41efaa…`; the ledger records the same r7-1 harness sha for the round-8 measurements. At 2227d83 the lane file has moved (fb91ef76…) — expected drift, which is what the monitor flagged.
- **Re-read paragraph.** The mado transient `dc864c6a…` is on record in fleet-kill-rate-ledger.md:338 as a working-tree transient later resolved into the committed chain — corroborated, though its byte size/mtime are no longer re-observable (scratch gone).
- **Falsifiers (executed, receipts 2 and 3).** Untouched scratch copy of kagi's branch-tip `corpus/surface-census.sh` hashes equal to the tip blob → `current`; the same copy with one line appended hashes differently → `drift`; substrate `git status --porcelain -- corpus/surface-census.sh` printed 0 lines after. `stale` verified in the siblings: each recorded revision is a `merge-base --is-ancestor` of today's `refs/heads/master` and the tip blob differs. The engine's doctored-pin refusal arm re-passed at the exact ticked bytes: `MUTATE_SELFTEST: 67/67 pass` / `VERDICT: PASS` (5-6 s; receipt 3), and the ticked tool's own selftest includes "unresolvable revision is SETUP (exit 2)" / "pin mismatch is SETUP (exit 2)", matching the current-row rule's parenthetical.

No tool installs or upgrades were needed. Verdict: the section is a record whose every pointer and observation I could re-derive checks out; the only gaps are the inherent non-recoverability of an October 14 scratch dir and the tool/tree drift the section itself predicts and prescribes handling for.

COLDREAD Read14: verified-record
