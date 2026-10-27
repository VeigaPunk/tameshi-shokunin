## Findings

- F1: “Live instances at round 8 (2026-10-14): tsukuroi `084951be…` (6/10) → `bba6cdf6…`; mado `d7edaab4…` (4/10) → `90d50cdd…` (both have moved again since; re-read, never carry).” is not a coherent statement of the records: the referenced mado run is 4/10 under `b56c6e57…`, not under pin `d7edaab4…` → `90d50cdd…`; the service protocol records this separately (`corpus/knowledge/service-optin-protocol.md:232`). Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:corpus/knowledge/service-optin-protocol.md`.

## Holds

- Checked 8 distinct pointer targets/anchors: ledger §5 lines 170–173; ledger re-pin rule lines 306–312; ledger ER-3/ER-4 cited lines 310, 318; service-optin protocol request shape lines 59–62 and precedent line 232; SKILL.md T1/T2/T3 surrounding historical context and citation anchors.
- The dated round-8 receipt and re-pin principle are supported by the cited ledger/SKILL text. No other failure found.
