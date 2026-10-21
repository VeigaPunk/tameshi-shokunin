# C08 — staged receipt-window exit map

## Result

**Agree** with the staged gate's declared exit map: clean `0`, findings `1`, could-not-evaluate `2`, usage `64`. The staged script SHA-256 was observed as `f03ae7e91607750e2690f7819c486a3d9db03ee13f0b8cf51958462834dcf7cc`, matching the frozen contract hash. No actionable defect was found in this scoped check.

## Fixtures and observations

Each fixture ran the staged script directly against temporary files under `/tmp/tameshi-r20-C08ExitMap-2k3u91hk/`; the temporary directory was automatically removed after the run. The clean/findings fixtures used a copy of the lane's frozen contract. The could-not-evaluate fixture used malformed contract JSON. Usage was invoked with no arguments as requested. First output lines are quoted exactly; `—` means that stream was empty.

| Class | Command | Exit | First stdout line | First stderr line |
|---|---|---:|---|---|
| Clean | `/usr/bin/python /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-20/stage/receipt-window.py --contract /tmp/tameshi-r20-C08ExitMap-2k3u91hk/contract.json --receipts /tmp/tameshi-r20-C08ExitMap-2k3u91hk/receipts.json` (one valid receipt using the contract's `f03ae7…f7cc` identity SHA and an aware interval) | `0` | `RECEIPT_WINDOW: CLEAN (receipts=1 historical=0)` | — |
| Findings | Same command; receipts fixture was `{"receipts": []}` | `1` | `RECEIPT_WINDOW: FAIL (findings=1 receipts=0)` | — |
| Could-not-evaluate | Same command; contract fixture was `{not json` | `2` | `RECEIPT_WINDOW: COULD_NOT_EVALUATE (CONTRACT_INVALID: cannot read contract: Expecting property name enclosed in double quotes: line 1 column 2 (char 1))` | — |
| Usage | `/usr/bin/python /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-20/stage/receipt-window.py` | `64` | — | `usage: receipt-window.py [-h] [--contract CONTRACT] [--receipts RECEIPTS]` |

## Verification gaps and boundaries

- These were the requested single fixtures per exit class, not an exhaustive malformed-input or gate-behavior suite.
- An `lsp` device is not mounted in this session: attempting to read `xd://lsp` returned `No such tool`. No LSP status/references/definition/diagnostics results are claimed.
- No package/tool install or update was performed. Fixtures and outputs were confined to the private `/tmp` sandbox; no lane production, staged evidence, Git/JJ state, or sibling files were written.