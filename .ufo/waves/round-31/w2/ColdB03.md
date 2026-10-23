# ColdB03 — wave-2 cold read (round 31)

Independent cold read of three SKILL.md sections at `2da841bd9913a2037d2bf612793382e572c9d205` (SKILL.md sha256 `2381873162fc21db756f8e8744d85aaa6dfc245a01175d5d5ac66557f617d35a`). Fleet-mirror clone kept detached at the read rev; sibling lanes reached read-only through the mirror symlinks. All section runs executed via `tools/trace-inputs.py` with literal `--out` names as listed per section.

```json
{
  "schema": "tameshi-coldread-report-v2",
  "seat": "ColdB03",
  "skill_sha256": "2381873162fc21db756f8e8744d85aaa6dfc245a01175d5d5ac66557f617d35a",
  "read_rev": "2da841bd9913a2037d2bf612793382e572c9d205",
  "sections": [
    {
      "start": 131,
      "heading": "## Mutation-sweep recipe — numbered steps; bounded cold-read evidence",
      "class": "instruction",
      "verdict": "gap-minor",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [
        "The B5/B10 survivor-probe expectations are cited at mutation-case-kagi-census.md:251-253 but the text sits at lines 252-254 (line 251 is blank) — a one-line offset on that range cite."
      ],
      "commands_executed": [
        "python3 -c \"import sys;[print('=== %s ==='%p, open(p,encoding='utf-8',errors='replace').read()[:4000]) for p in sys.argv[1:]]\" corpus/knowledge/mutation-case-kimi-census.md corpus/knowledge/mutation-case-kagi-census.md corpus/knowledge/gates-survey-kumitate.md corpus/knowledge/gates-survey-kagi.md corpus/README.md",
        "git status --porcelain -- corpus/knowledge/mutation-case-kimi-census.md corpus/knowledge/mutation-case-kagi-census.md corpus/README.md",
        "python3 -c \"import subprocess,hashlib,sys,os; R=os.getcwd(); rev='2da841bd9913a2037d2bf612793382e572c9d205'; [print(p, hashlib.sha256(subprocess.run(['git','-C',R,'show',rev+':'+p],capture_output=True).stdout).hexdigest()) for p in sys.argv[1:]]\" corpus/knowledge/mutation-case-kimi-census.md corpus/knowledge/mutation-case-kagi-census.md corpus/knowledge/gates-survey-kumitate.md corpus/knowledge/gates-survey-kagi.md corpus/README.md corpus/QUALITY.md corpus/SOURCES.md corpus/lessons/round-20.md corpus/knowledge/mutation-case-kumitate-cite-check.md .ufo/evidence/round-26/cite-check/sweep/sweep.txt .ufo/evidence/round-20/contract.json .ufo/evidence/round-20/final/receipts.json .ufo/evidence/round-20/stage/measure.py .ufo/evidence/round-20/public-cli-cases.json tools/receipt-window.py tools/receipt-measure.py .ufo/evidence/round-20/coldread/measure.py .ufo/waves/round-26/w1/ProbeSOOREDGE.md .ufo/waves/round-26/w1/ProbeSSTRICT.md .ufo/waves/round-26/w1/ProbeSUSAGE.md .ufo/waves/round-26/w1/ProbeSPININCLUDES.md .ufo/waves/round-26/w1/ProbeSEMPTYGUARD.md .ufo/waves/round-26/w1/ProbeIntegrations.md .ufo/waves/round-26/w1/CriticEquivalence.md"
      ],
      "opened": [
        "corpus/knowledge/mutation-case-kimi-census.md",
        "corpus/knowledge/mutation-case-kagi-census.md",
        "corpus/knowledge/gates-survey-kumitate.md",
        "corpus/knowledge/gates-survey-kagi.md",
        "corpus/README.md"
      ],
      "inputs": {
        "corpus/knowledge/mutation-case-kimi-census.md": "034524eff8f19cb8fca78cd5d13c6da9971f2ef2b5bedc1b950309c95c121548",
        "corpus/knowledge/mutation-case-kagi-census.md": "d3190a9940b9d47b7aae0025b2f4c80228d5a15cbb052cbef316ddff021d0bb0",
        "corpus/knowledge/gates-survey-kumitate.md": "3dca7a1a5c621bf0ec75948d0836839dec98651673bb2987861d9aa122579b0e",
        "corpus/knowledge/gates-survey-kagi.md": "4734f0a0bd28e90f78b0a766b2aa6dac8238936550e1b1b0ec3316b00e1294c6",
        "corpus/README.md": "0b68064b9d65a93eb8abfbcd86736cff927f827894d643449e413b3aa7212cbd"
      },
      "external_inputs": {},
      "traces": [
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdB03-1-1.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdB03-1-2.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdB03-1-3.json"
      ]
    },
    {
      "start": 1938,
      "heading": "### Round-20 gate/probe registry — frozen receipt instruments",
      "class": "record",
      "verdict": "verified-record",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [],
      "commands_executed": [
        "python3 -c \"import sys;[print('=== %s ==='%p, open(p,encoding='utf-8',errors='replace').read()[:4000]) for p in sys.argv[1:]]\" corpus/lessons/round-20.md corpus/QUALITY.md corpus/SOURCES.md tools/receipt-window.py tools/receipt-measure.py .ufo/evidence/round-20/coldread/measure.py .ufo/evidence/round-20/contract.json .ufo/evidence/round-20/final/receipts.json .ufo/evidence/round-20/stage/measure.py .ufo/evidence/round-20/public-cli-cases.json",
        "python3 tools/receipt-window.py --selftest",
        "python3 tools/receipt-measure.py --selftest",
        "python3 .ufo/evidence/round-20/coldread/measure.py --selftest",
        "python3 tools/receipt-window.py --contract .ufo/evidence/round-20/contract.json --receipts .ufo/evidence/round-20/final/receipts.json --json"
      ],
      "opened": [
        "corpus/lessons/round-20.md",
        "corpus/QUALITY.md",
        "corpus/SOURCES.md",
        "tools/receipt-window.py",
        "tools/receipt-measure.py",
        ".ufo/evidence/round-20/coldread/measure.py",
        ".ufo/evidence/round-20/contract.json",
        ".ufo/evidence/round-20/final/receipts.json",
        ".ufo/evidence/round-20/stage/measure.py",
        ".ufo/evidence/round-20/public-cli-cases.json",
        ".ufo/evidence/round-18/measure.py"
      ],
      "inputs": {
        "corpus/lessons/round-20.md": "7dab5fc4c3e18153c919fd46f5c2d534ccf2ff0904462177d6e31fe2ceb31dc6",
        "corpus/QUALITY.md": "6cbf9cf7a9117a747be356f7ac5ed8288c8609195205bcca427809b4d96804ac",
        "corpus/SOURCES.md": "489ee8af2ddc835afb4988e311be20aba6638de9ed407f8c440691516311a741",
        "tools/receipt-window.py": "f03ae7e91607750e2690f7819c486a3d9db03ee13f0b8cf51958462834dcf7cc",
        "tools/receipt-measure.py": "a67bffa9c562ee1c22e8fbd580668379b452e63df82ee6141fe54623d5931afa",
        ".ufo/evidence/round-20/coldread/measure.py": "48927bfeaf9c70108270e022478366bfdb2a47821724eaba1001aefe1264fe13",
        ".ufo/evidence/round-20/contract.json": "9b2813342768fdaa51bfd670a19d8573f87169a59b98207200e622f8e2b62715",
        ".ufo/evidence/round-20/final/receipts.json": "4186b44e6f5ef95aeb39768e5b9d8a0e6953283961bcc009733dbbcde48cb5d6",
        ".ufo/evidence/round-20/stage/measure.py": "f34dc233eee33f4fea9a82c391bfb57ebfef8983f5c7146b4d2dc0b6b3be4e2d",
        ".ufo/evidence/round-20/public-cli-cases.json": "590df60420a60bec1f6dddad6b5eaf34a5d700cdd86c5cf231b1ef8f5a3b27b2",
        ".ufo/evidence/round-18/measure.py": "7ca87a7c98196d87a86627cf96e2e9bc7b3a8769496a75ce8caca1955b26dd37"
      },
      "external_inputs": {},
      "traces": [
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdB03-8-1.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdB03-8-2.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdB03-8-3.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdB03-8-4.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdB03-8-5.json"
      ]
    },
    {
      "start": 2104,
      "heading": "## Ninth recorded case — round 26",
      "class": "record",
      "verdict": "verified-record",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [],
      "commands_executed": [
        "python3 -c \"import sys;[print('=== %s ==='%p, open(p,encoding='utf-8',errors='replace').read()[:4000]) for p in sys.argv[1:]]\" .ufo/evidence/round-26/cite-check/sweep/sweep.txt corpus/knowledge/mutation-case-kumitate-cite-check.md corpus/SOURCES.md",
        "python3 -c \"import subprocess,hashlib,sys; rev=sys.argv[1]; blob=sys.argv[2]; d=subprocess.run(['git','-C','../kumitate-shokunin','show',rev+':'+blob],capture_output=True).stdout; print('bytes',len(d),'lines',len(d.splitlines()),'sha256',hashlib.sha256(d).hexdigest())\" 1205c6621a2eccbb8ffceae86d9e7b79a7990b3a scripts/cite-check.mjs",
        "python3 -c \"import subprocess,sys; r=subprocess.run(['git','-C','../kumitate-shokunin','ls-tree',sys.argv[1],sys.argv[2]],capture_output=True); print(r.stdout.decode())\" 1205c6621a2eccbb8ffceae86d9e7b79a7990b3a scripts/cite-check.mjs",
        "python3 -c \"import subprocess,sys; b=subprocess.run(['git','-C','../kumitate-shokunin','cat-file','blob',sys.argv[1]],capture_output=True).stdout; print('wc_lines',b.count(b'\\n'),'endswith_nl',b.endswith(b'\\n'),'tail',b[-40:])\" 9770de8c5a834b2f2adb817f8b0a7ba9e166b87f",
        "timeout 380 bash /fast/scratch/hyaku/tameshi-r31-seats/ColdB03/fleet/tameshi-shokunin/tools/mutate-and-run.sh --regression --workdir /fast/scratch/hyaku/tameshi-r31-seats/ColdB03/rg-10"
      ],
      "opened": [
        ".ufo/evidence/round-26/cite-check/sweep/sweep.txt",
        "corpus/knowledge/mutation-case-kumitate-cite-check.md",
        "corpus/SOURCES.md",
        ".ufo/waves/round-26/w1/ProbeSOOREDGE.md",
        ".ufo/waves/round-26/w1/ProbeSSTRICT.md",
        ".ufo/waves/round-26/w1/ProbeSUSAGE.md",
        ".ufo/waves/round-26/w1/ProbeSPININCLUDES.md",
        ".ufo/waves/round-26/w1/ProbeSEMPTYGUARD.md",
        ".ufo/waves/round-26/w1/ProbeIntegrations.md",
        ".ufo/waves/round-26/w1/CriticEquivalence.md"
      ],
      "inputs": {
        ".ufo/evidence/round-26/cite-check/sweep/sweep.txt": "957952b8f4e3cb413b73af8830c17705b480b702807c269eda7a1bc148ad1893",
        "corpus/knowledge/mutation-case-kumitate-cite-check.md": "a58bc159ef5b7eed9b42ad40c57a2c46d6ebfc898f530dbde790afc5f03fd34e",
        "corpus/SOURCES.md": "489ee8af2ddc835afb4988e311be20aba6638de9ed407f8c440691516311a741",
        ".ufo/waves/round-26/w1/ProbeSOOREDGE.md": "c0cd5194f6162f2f6d91531f0a512eace80cf2028b8f25505d45b8e976af4e04",
        ".ufo/waves/round-26/w1/ProbeSSTRICT.md": "19ef870f885ce37fb9f34570347fe87f034913ba465491df1950a878fea98153",
        ".ufo/waves/round-26/w1/ProbeSUSAGE.md": "d82bb2823e63952fa7614da1bd2ea359e902f1fa719844f5386f75de53a4beeb",
        ".ufo/waves/round-26/w1/ProbeSPININCLUDES.md": "bc297eb2ae9ad42e504cfd2777627147988b146b3ad6cebce122a068bd2d5a5c",
        ".ufo/waves/round-26/w1/ProbeSEMPTYGUARD.md": "7be4dc4cf29ee7d62c6a494627cafb33d2035072c174189b00bd52753b96ccd9",
        ".ufo/waves/round-26/w1/ProbeIntegrations.md": "ac1b2c47e6a3e39ebadcb4c36cc421007e4e43fd61f836e02b0e2d2c95f1006b",
        ".ufo/waves/round-26/w1/CriticEquivalence.md": "575ef324cba9b25c56ad8dd4ea4d251fb2c4941505a11b76b25a777f10d22285"
      },
      "external_inputs": {
        "kumitate-shokunin@1205c6621a2eccbb8ffceae86d9e7b79a7990b3a:scripts/cite-check.mjs": "40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f"
      },
      "traces": [
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdB03-9-1.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdB03-9-2.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdB03-9-3.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdB03-9-4.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdB03-9-5.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdB03-9-6.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdB03-9-7.json"
      ]
    }
  ]
}
```

## What I checked

**Section 1 (instruction, `## Mutation-sweep recipe`)** — Recipe claim-by-claim ground against the two historical case notes, the kumitate/kagi gates surveys, and `corpus/README.md` G-R2-1. Killed the control claim (43/43 + `VERDICT: PASS` exit 0), 8/10 + 11 runs in 7.0 s (round 2), 16 enumerated cases with 14 executed / 2 skipped (round 3), driver `--check`/`all unique`, restore pins (sha256 before=after `83016d45…` / `275d8294…`, `cmp`), survivor probes D2/D10/B5/B10 (including `SURFACE OK … (exec 644)` vs `SURFACE DIVERGED … no execute bit` and `ok=0` vs `ok=1`), the E1 calibration records, and the exact failing-case label strings. Executed a named recipe command (`git status --porcelain -- <paths>`, exit 0, empty). One genuine minor gap: the B5/B10 sensitivity-expectation cite lands at lines 251-253 while the text sits at 252-254 (line 251 blank). Full end-to-end sweep (steps 5-8) was not re-run here: the historical drivers are unversioned and the section itself redirects maintained replay to `mutate-and-run.sh --regression`; the pinned facts the steps rest on all verified against the notes.

**Section 8 (record, `### Round-20 gate/probe registry`)** — Source and criteria located (round-20.md; QUALITY41 at QUALITY.md:390; S049 row). Executed all three registered self-tests: receipt-window 20/20, receipt-measure 10/10 (reports runner SHA `a67bffa9…` and instrument SHA `f34dc233…`, matching the contract frozen sha and the final receipts' `runner_sha256`/`instrument_sha256`), selector 12/12 (abbreviation and equals-form override refusals covered). Executed the exact entry command from the registry: `python3 tools/receipt-window.py --contract .ufo/evidence/round-20/contract.json --receipts .ufo/evidence/round-20/final/receipts.json --json` → exit 0, `CLEAN`. Confirmed the staged `stage/measure.py` bytes equal the contract's frozen `f34dc233…` (byte preservation), the installed gate equals `f03ae7e9…`, the ruler hardcodes six predicates, and the `--check` spelling is refused (usage exit 2) while `--json` works.

**Section 9 (record, `## Ninth recorded case — round 26`)** — Pinned kumitate blob at `1205c662…` via the mirror: blob sha256 `40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f`, 126,735 bytes, mode 100755, and 2537 `wc -l` newlines (final line unterminated — same convention as the kagi 886-newline note; the entry's "2,537 lines" holds under `wc -l`). Sweep receipt: 5 killed / 5 survived, 50 %, control `62/62 cases passed (hermetic)`; entry table shows 10/10 predictions held (killing cases named), pre-registration `622d31d` (10:01:47Z) before sweep (10:02:07Z). Survivor probes exist and carry hermetic off-suite witnesses for the four holes; `S_EMPTY_GUARD` equivalence argument verified (structural proof + 316/316 differential runs); integrations probe shows none of the five killed and the pristine integration group red. Executed the replay command: `REGRESSION_CASE js-cite-check: PASS` and `REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)` (ran in ~320 s under the trace collector, within the 6-minute bound).

Trace receipts 9-2/9-3 were initial verification runs using the relative path `fleet/kumitate-shokunin`, which does not exist from inside the clone (`$R` is itself under `fleet/`); they exited 0 with empty verification output and were superseded by 9-4/9-5/9-7 using `../kumitate-shokunin`. All receipts list argv exactly as executed and `rev` = read rev.

COLDREAD ColdB03: gap-minor, verified-record, verified-record
