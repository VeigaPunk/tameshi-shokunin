## Findings

None. Every statement and pointer in the section holds at CAND1; `findings` is `[]`.

## Holds

1. `SKILL.md:1069-1090` is in the round-8 cadence section and includes the T1 rule at `:1071-1072`; it records two instances at `:1073-1074`. Checked with `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:SKILL.md | sed -n '1069,1090p'`.
2. `corpus/knowledge/service-optin-protocol.md:59-62` contains the quoted re-pin rule in the request-shape body, not only in errata. Checked with `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:corpus/knowledge/service-optin-protocol.md | sed -n '59,62p'`.
3. `corpus/knowledge/fleet-kill-rate-ledger.md` exists; its append-only discipline and unchanged recorded tables are supported by `:239`, `:312`, and `:318`. Checked with `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:corpus/knowledge/fleet-kill-rate-ledger.md | sed -n '239p;312p;318p'`.
4. The rate-per-revision statement holds at ledger `:312`. Checked with the same CAND1 `git show` command, selecting line 312.
5. ER-4 names the two moved-case re-sweeps as follow-on rows at ledger `:339` and `:352`. Checked with `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:corpus/knowledge/fleet-kill-rate-ledger.md | sed -n '318,352p'`.
6. ER-4's addendum records both as `stale + drift` at ledger `:358-359`; checked with the same CAND1 `git show` command, selecting lines 354-362.
7. Those re-sweeps remain open at CAND1: ledger `:398-401` says successor sweep joins tsukuroi/mado debt and the disposition closes no mutation re-sweep. Checked with `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:corpus/knowledge/fleet-kill-rate-ledger.md | sed -n '366,401p'`.
8. The unlanded follow-ups are named, not assumed: ledger `:282` names follow-ups and `:398` calls the successor sweep debt. Checked with the same CAND1 `git show` command, selecting lines 272-283 and 396-401.

**Holds checked: 8.** The section is lines 1230-1245 inclusive (16 lines, including the final blank); SHA-256 of those lines joined with `\n`: `22e828f50b3e3ce92e9e500a3ead897308e8ad99e5f3bf3d6747784f59c71c15`.

## Summary

- No failing statements or stale pointers found.
- All 8 listed checks hold at CAND1.
