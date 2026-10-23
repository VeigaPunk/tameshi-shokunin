# Read12A — cold read, SKILL.md:1964

Round-21 gate/probe registry — finite environment differential, read at 9f3084bc60ad56aac01e4556ef4c7653df2f65e5.

```json
{"schema": "tameshi-coldread-report-v2", "seat": "Read12A", "skill_sha256": "c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6", "read_rev": "9f3084bc60ad56aac01e4556ef4c7653df2f65e5",
  "sections": [{"start": 1964, "heading": "### Round-21 gate/probe registry — finite environment differential", "class": "record", "verdict": "verified-record", "blocking_gaps": [], "wrong_expectations": [],
  "minor_gaps": [],
  "commands_executed": [
    "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/lessons/round-21.md corpus/knowledge/hermetic-env-differential.md",
    "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/knowledge/callback-authoritative-accounting.md corpus/knowledge/required-command-binding.md corpus/knowledge/replay-projection-hardening.md",
    "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/lessons/round-24.md .ufo/evidence/round-21/c2-contract.json .ufo/evidence/round-21/f5/receipt.json .ufo/waves/round-21/routemix-spec1.json",
    "python3 tools/wave-accounting.py --selftest",
    "python3 tools/wave-accounting.py --bundle .ufo/evidence/round-22/bundle.json --expected .ufo/evidence/round-22/expected.json --json",
    "python3 tools/wave-accounting.py --bundle .ufo/evidence/round-22/wrong-count-bundle.json --expected .ufo/evidence/round-22/wrong-count-expected.json --json",
    "python3 tools/command-binding.py --selftest",
    "python3 tools/command-binding.py --bundle .ufo/evidence/round-23/replay/bundle.json --expected .ufo/evidence/round-23/replay/expected.json --json",
    "python3 .ufo/evidence/round-23/replay.py --repo /tmp/Read12A-C4Mj/fleet/tameshi-shokunin --rev 9f3084bc60ad56aac01e4556ef4c7653df2f65e5 --out /tmp/Read12A-replay-out --json",
    "python3 -c \"import re;print('== QUALITY ==');[print(l,end='') for l in open('corpus/QUALITY.md') if re.search(r'QUALITY4[3-9]',l)];print('== SOURCES ==');[print(l,end='') for l in open('corpus/SOURCES.md') if re.search(r'\\bS0(28|79|80|81|82|83|84|85)\\b',l)]\"",
    "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" .ufo/evidence/round-21/c2-count.py tools/round21-measure.py .ufo/evidence/round-21/coldread/measure.py",
    "python3 -c \"import json; reg=json.load(open('tools/registry.json')); rows=reg['rows'] if isinstance(reg,dict) and 'rows' in reg else reg; act=[r for r in rows if r.get('status','active')=='active']; print('registry rows',len(rows),'active',len(act)); b=json.load(open('.ufo/evidence/round-24/replay/bundle.json')); print('replay bundle receipts',len(b['receipts'])); o=json.load(open('.ufo/evidence/round-24/replay/observations.json')); print('obs rows',len(o['rows'])); l=json.load(open('.ufo/evidence/round-24/replay/live-dependent.json')); print(json.dumps(l)); g=json.load(open('.ufo/evidence/round-24/replay-gate.json')); print('gate',json.dumps({k:g[k] for k in ('exit','finding_ids') if k in g})); n=json.load(open('.ufo/evidence/round-24/noharm-c8c5b88.json')); print('noharm',json.dumps(n)[:500])\"",
    "python3 tools/registry-replay.py --selftest",
    "python3 tools/env-diff.py --selftest",
    "python3 -c \"import json,collections; d=json.load(open('.ufo/evidence/round-21/f5/receipt.json')); print(collections.Counter(s['classification'] for s in d['surfaces'])); print('clean exits:', set(s['profiles']['clean']['exit'] for s in d['surfaces']))\"",
    "python3 -c \"import re;[print(l,end='') for l in open('corpus/QUALITY.md') if re.search(r'QUALITY ?4[0-9]|^## ',l)]\"",
    "python3 .ufo/evidence/round-21/coldread/measure.py --selftest",
    "python3 tools/command-binding.py --bundle .ufo/evidence/round-23/source-read-bundle.json --expected .ufo/evidence/round-23/source-read-expected.json --json",
    "python3 -c \"import json\nfor p in ['.ufo/waves/round-21/routemix-spec2.json','.ufo/waves/round-21/routemix-spec1.json']:\n    d=json.load(open(p)); print(p, json.dumps(d)[:400])\"",
    "python3 -c \"print(open('.ufo/evidence/round-21/routemix-r20-spec1.exit').read()); print(open('.ufo/evidence/round-21/routemix-r20-spec1.json').read()[:600]); print(open('.ufo/evidence/round-21/routemix-r20-spec1.stderr').read()[:400])\""
  ],
  "opened": [
    "corpus/lessons/round-21.md", "corpus/lessons/round-24.md", "corpus/knowledge/hermetic-env-differential.md", "corpus/knowledge/callback-authoritative-accounting.md", "corpus/knowledge/required-command-binding.md", "corpus/knowledge/replay-projection-hardening.md",
    "corpus/QUALITY.md", "corpus/SOURCES.md",
    ".ufo/evidence/round-18/measure.py", ".ufo/evidence/round-21/c2-count.py", ".ufo/evidence/round-21/c2-contract.json", ".ufo/evidence/round-21/coldread/measure.py", ".ufo/evidence/round-21/f5/receipt.json", ".ufo/evidence/round-21/routemix-r20-spec1.exit", ".ufo/evidence/round-21/routemix-r20-spec1.json", ".ufo/evidence/round-21/routemix-r20-spec1.stderr",
    ".ufo/evidence/round-22/accounting-extra-cases.json", ".ufo/evidence/round-22/bundle.json", ".ufo/evidence/round-22/expected.json", ".ufo/evidence/round-22/measure.py", ".ufo/evidence/round-22/wrong-count-bundle.json", ".ufo/evidence/round-22/wrong-count-expected.json",
    ".ufo/evidence/round-23/extra-cases.json", ".ufo/evidence/round-23/replay.py", ".ufo/evidence/round-23/replay/bundle.json", ".ufo/evidence/round-23/replay/expected.json", ".ufo/evidence/round-23/source-read-bundle.json", ".ufo/evidence/round-23/source-read-expected.json",
    ".ufo/evidence/round-24/extra-cases.json", ".ufo/evidence/round-24/noharm-c8c5b88.json", ".ufo/evidence/round-24/replay-gate.json", ".ufo/evidence/round-24/replay/bundle.json", ".ufo/evidence/round-24/replay/live-dependent.json", ".ufo/evidence/round-24/replay/observations.json",
    ".ufo/waves/round-21/routemix-spec1.json", ".ufo/waves/round-21/routemix-spec2.json",
    "tools/command-binding.py", "tools/env-diff.py", "tools/registry-replay.py", "tools/registry.json", "tools/round21-measure.py", "tools/wave-accounting.py"
  ],
  "inputs": {
    ".ufo/evidence/round-18/measure.py": "7ca87a7c98196d87a86627cf96e2e9bc7b3a8769496a75ce8caca1955b26dd37",
    ".ufo/evidence/round-21/c2-contract.json": "5bd7024d0357ad3fb2a4b8550fd44f8371a3eb004f29948699368bea9d4c2bbd",
    ".ufo/evidence/round-21/c2-count.py": "9a34f77d8ae2e219c51c74d60695703ea3efe4f6745ba4b57da2dca2173520a2",
    ".ufo/evidence/round-21/coldread/measure.py": "657f009bdf1cc89ac614ed7c8424858f5f802b5a5330d8917db788f67982f3eb",
    ".ufo/evidence/round-21/f5/receipt.json": "9c61cc717b3d074f4eca750a1dda4151b10bfbe99f099642aec161027aa85264",
    ".ufo/evidence/round-21/routemix-r20-spec1.exit": "cf205dbb8cea84897b488abcc281bf96698d5e94b1096b16657b4caba9082a22",
    ".ufo/evidence/round-21/routemix-r20-spec1.json": "b43bd8943448c1ae918b5ce51c976f33829450b2650fd3242d6033be7c6eca7b",
    ".ufo/evidence/round-21/routemix-r20-spec1.stderr": "88e99fc2d6ad8560d28248ea0717076ca0620e07184d52261b2483ccae6494c5",
    ".ufo/evidence/round-22/accounting-extra-cases.json": "e60807f2154164638b13709af930760d0f16c2c8c4a2dee7297a490c5338a41f",
    ".ufo/evidence/round-22/bundle.json": "dfb1027f80be935fe781ccb8c47d89639a88a9eff6e05d1b45b2a7a61845c18e",
    ".ufo/evidence/round-22/expected.json": "e35a5934afa0ace85aeba5e687c8e12b7c7c2258af9cd00d76c13f8c0975457d",
    ".ufo/evidence/round-22/measure.py": "f833d067afd3ca17b8534fc942d6e8ed529edd3d55476802c18ea631c0678056",
    ".ufo/evidence/round-22/wrong-count-bundle.json": "d984c49c57d2b12b3a4e2583cc33842af6927f0612b3b0d663acb2ca09a7a17e",
    ".ufo/evidence/round-22/wrong-count-expected.json": "caf7d29e0fea8e8492152d3798201069452019928d6dd58ba052d98e6d0ad0ec",
    ".ufo/evidence/round-23/extra-cases.json": "87bffdc829ad705c9fad6c4c0495e50e1bc5c6d2af3fec04da2294fda43c1c00",
    ".ufo/evidence/round-23/replay.py": "adb4171652f954d460c5e0c86d8baa4fcfa2f7fdd0b87791995afb601ae22c11",
    ".ufo/evidence/round-23/replay/bundle.json": "3d6c99b70b3e30b9dc4c25c327d90d956e069836ddcc6e024180cbc6267a50b9",
    ".ufo/evidence/round-23/replay/expected.json": "0831c9c820488dc9d9096c90aade44217b6b615501fae7810e6fce414cb2a0a1",
    ".ufo/evidence/round-23/source-read-bundle.json": "db620668efe12c00f55518b993c3ffd20dc254f3ace8f06bc82bb661a580d3cf",
    ".ufo/evidence/round-23/source-read-expected.json": "70f357e354c4badb22f974070ccf37dfda512103c3cf3ab93297a3ea27cb5dc8",
    ".ufo/evidence/round-24/extra-cases.json": "6ad7842fa01fc205bb92f0989f87fcaa88a3b79078a9c4302647a321f359cb35",
    ".ufo/evidence/round-24/noharm-c8c5b88.json": "83e95c2210c8f22bc92fe8884fcd7a497727085348e3ff882ecea7a5bdebb21a",
    ".ufo/evidence/round-24/replay-gate.json": "73ca96f01835362a3a6351460dfaffacc2224b1c941e76e1d09cb15c941d9172",
    ".ufo/evidence/round-24/replay/bundle.json": "4f4240230d4faecb54f488bb0d889de472e4e3f97e693e9304288429a722a9c6",
    ".ufo/evidence/round-24/replay/live-dependent.json": "c3a5f9133f6f90a2da337873b26b4bae9b09a397b7a1abdaeee6ce003b9a4ef3",
    ".ufo/evidence/round-24/replay/observations.json": "2d9b1b77349bf148095a80bfd7ef9c98f8584b7a0c7c261a0d406896a69a7a88",
    ".ufo/waves/round-21/routemix-spec1.json": "92c1edb3fdf53ac45bb6d324c16d94b388c26960aceee53f74f6883af1b97d56",
    ".ufo/waves/round-21/routemix-spec2.json": "9bf8554f1967df87cba8a5d97047089673d84ce9fffccfab5a80f464a2edbb51",
    "corpus/QUALITY.md": "069ef729b7738927585f487afa3c26b4912b9d568cb9f0c69b00c3f172538e07",
    "corpus/SOURCES.md": "804f0b4369e87fa87a45f194e8cbb315d7ea7af56957fd4c26775eddd3751dca",
    "corpus/knowledge/callback-authoritative-accounting.md": "ddf13b0835a5e6c21c308ab87ec24c9d8eee8bb8af3b3b254d73b554e9cf6035",
    "corpus/knowledge/hermetic-env-differential.md": "90756351093e2273257ce6a738bb90b6923865bc22d9276ba2cf8aeafb262e7e",
    "corpus/knowledge/replay-projection-hardening.md": "7602943988d8c7a2ce566b810b28d98c01938c565244be2503bee295d76520f4",
    "corpus/knowledge/required-command-binding.md": "2e72f8a04017b6d16e67ebd8e9e8bdb5d45b70701030a3f5466b187369ab4fd6",
    "corpus/lessons/round-21.md": "35444ddc32116089f87733c8f0a635dc7b452407d2bd0f47de483e8aacfb1a7d",
    "corpus/lessons/round-24.md": "29fd3e00a79242536bc259f6d56d6473e5e0d1e5bf451413c061fb6094b7d7a6",
    "tools/command-binding.py": "9230c68e53a544c517037620f32ea98528e5b5195f88fd88e976fdc8c1061d0d",
    "tools/env-diff.py": "e8b47ab7cf2323764d9e9d3519352cd75e1abda4d5e98e7df602dc23bc099ead",
    "tools/registry-replay.py": "9fcd2dbba737f0b1b412a9c955fe78e2bb7ea316bf56f98b40a475def5208714",
    "tools/registry.json": "c1b75366f1789121e6d5a4c8f6587f7519fef3bad60569ed274df8c7a681b73c",
    "tools/round21-measure.py": "eda5490acd447cd9eeac3ab10a348565b34d8a6fa2800d66a4fb1c80c162758d",
    "tools/wave-accounting.py": "96b3038a77f895c119b6e88d8b1278effffd1cebcc7dc18e6bd7a080a1bafd8e"
  },
  "external_inputs": {},
  "traces": [
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read12A-1.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read12A-2.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read12A-3.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read12A-4.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read12A-5.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read12A-6.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read12A-7.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read12A-8.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read12A-9.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read12A-11.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read12A-12.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read12A-13.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read12A-14.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read12A-15.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read12A-16.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read12A-17.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read12A-18.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read12A-19.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read12A-20.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read12A-21.json"
  ]}]}
```

What I checked, in brief:

- Classed `record`: the section states registry facts with pointers; its own Round-28 correction says receipts, not re-runs, are the round-21 record. The reader commands above are the traced record reads; the selftests and gate runs are extra verification of claims the section itself marks runnable.
- `tools/env-diff.py --selftest` printed `ENVDIFF_SELFTEST: 9/9 pass` (the section's round-21 table and lesson both claim 9/9).
- `tools/wave-accounting.py --selftest` printed 8/8 `ACCOUNTING_SELFTEST` plus 16/16 `ACCOUNTING_EXTRA_SELFTEST`, matching "eight literal public-CLI rejection fixtures ... plus 16 further schema/accounting guards". The clean bundle exited 0 with `finding_ids: []`; the wrong-count pair exited 1 with `TOTAL_MISMATCH` (claimed 40/35 vs observed 38/37), matching the "expected verdict is 1/TOTAL_MISMATCH" line. The bundle totals 146/66/80 match the lesson's corrected accounting.
- `tools/command-binding.py --selftest` printed 44/44, matching registry row `command-binding-selftest-r24` (44/44). The round-23 replay bundle is clean (`{"exit":0,"finding_ids":[]}`, bundle_sha256 3d6c99b7..., the exact literal pinned in `command-binding-frozen-clean-pinned`); the source-read pair exits 1/`ARGV_MISMATCH` with digest db620668..., the literal pinned in `command-binding-source-read-red-pinned`.
- `tools/registry-replay.py --selftest` printed 10/10, matching `registry-replay-selftest` (10/10).
- `.ufo/evidence/round-21/coldread/measure.py --selftest` printed 12/12 including all nine override refusals (SELECTOR_OVERRIDE_FORBIDDEN at exit 64), matching the verdict map.
- Static claims in the Round-28 correction: `c2-count.py:19` is `FLEET = Path("/home/vgpnk/Projects/shokunin")` and `:52` is `blob = show(FLEET / frozen["repo"], want_rev, frozen["path"])` — the fleet-root read that makes `--claim c2`/`--selftest` non-hermetic, exactly as stated. Per the section itself I did not re-run the facade (it reads live lane objects); receipts are the record.
- Round-24 replay evidence: `live-dependent.json` is exactly `["pin-disposition-read","verify-round15"]` with `revision_pinned: 41, rows: 43`; `replay/bundle.json` has 43 receipts; `replay-gate.json` exit 0 — "covers all 43 stored receipts, including both declared-live rows". `tools/registry.json` has 56 rows, 49 active ("49 active rows from round 26 on"), with superseded `command-binding-selftest` expecting 38/38 — and the live tool now prints 44/44, so the superseded row does fail as stated.
- `f5/receipt.json` classification counts: 8 invariant + 1 nondeterministic (`js-round-gate`), all nine clean exits 0 — matches "eight raw-tuple invariant surfaces and one raw-output-nondeterministic surface" and the round-gate random-path caveat.
- Routemix receipts: `.ufo/evidence/round-21/routemix-r20-spec1.exit` is `exit=1` with `ROUTEMIX: REFUSE` over `openai-codex` (35/72 > 0.40); `.ufo/waves/round-21/routemix-spec1.json` is `ok: true` (28/71 codex) — "round20 refused spec/round21 accepted spec retained" verified.
- Source pointers resolve in `corpus/SOURCES.md` at this rev despite its drift: S079 (mined, used-by hermetic-env-differential), S028 (mined, reopened per round-21 lesson — status stays mined with updated used-by), S081 (mined, supersedes S028 wording), S082/S083/S084/S085 (all mined, used-by the named knowledge entries and lessons). QUALITY items 43–49 exist as numbered criteria 43–49 in QUALITY.md and match the cited content (43 provider share/0.40, 44 anchor re-anchoring, 45 callback-authoritative accounting, 46 required-command binding, 47 correction narrowing 46, 48/49 round-24 predicates). `corpus/lessons/round-24.md` contains Errata E–P and the residual corrections named as "full limitations and evidence".
- Skipped named commands: `tools/round21-measure.py --claim c1|c2` and its `--selftest` (reads live lane Git objects via the `FLEET` constant, which the section itself documents; the assignment forbids reading the live lane during traces and the section says receipts are the record). `tools/wave-route-mix.py --spec ... --json` live re-run (reads the operator's live route table; the section says the retained receipt, not a re-run, is the record). `.ufo/evidence/round-23/replay.py` full run was started under the collector but exceeded ~5 minutes and was killed at the cap (>6 min bound); its `--json` usage error run exited 2 and is receipted (Read12A-9). None of these gaps contradict the section; they are documented live-read or long-running instruments whose retained receipts I verified instead.

COLDREAD Read12A: verified-record
