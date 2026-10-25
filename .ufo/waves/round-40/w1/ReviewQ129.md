# ReviewQ129 — hand-check quarantined S129

## Verdict: PRESENT (row verifies; the register's flagged quote is an extraction artifact, not a fabrication)

## The row under check

- Register row: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md:222`
  `tameshi | round3 | S129 | payload-absent | https://www.t.kyoto-u.ac.jp/lib/ja/support/ieice | canonical`
- Census record: `quote-lint-full-v5.json` `findings/1686` — `id: S129, verdict: ABSENT, quote: "canonical", line: "declared in the page's own og:url and link rel=\"canonical\")"` (`sweep: false, binding: id`).
- The row is the Kyoto Katsura Library IEICE-技報アーカイブ access page, staged in the lane round-3 corpus as S133 after the packaging remap (`/home/vgpnk/Projects/shokuknow/lanes/tameshi/ID-REMAP.md`: `round3 | S129 → S133`; merge append row at `/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md:31`).

## Fetch evidence (2026-10-24)

Command: `curl -fsSL 'https://www.t.kyoto-u.ac.jp/lib/ja/support/ieice' -o /tmp/tameshi-r40-ReviewQ129/ieice.html`

- HTTP fetch succeeded; 31,355 bytes; sha256 `310c1074d5f335e2bb2a1e384d5595e6ad3c7d9452294833dad1f394d40f6c9b`.
- `grep -c 'canonical' ieice.html` → **1**: `<link rel="canonical" href="https://www.t.kyoto-u.ac.jp/lib/ja/support/ieice" />`; `og:url` content is the same URL. The row's prose claim — "the canonical URL is declared in the page's own `og:url` and `link rel=\"canonical\"`" (`/home/vgpnk/Projects/shokuknow/lanes/tameshi/round3/SOURCES-PROPOSED.md:45-47`) — is **true in the fetched bytes**.
- Tag-stripped visible text does **not** contain the token `canonical`. The flagged "quote" is a code token captured from a parenthetical provenance note, not a quoted span asserting page content. Even under a literal raw-byte quote test, the string is present; ABSENT holds only for tag-stripped text, where it was never claimed.
- The row's two real gate quotes verify: `技報オンラインシステムログインURL` verbatim in visible text; the boxed notice `2026年4月1日から、「技報アーカイブ」は、IPアドレス制から【ID/パスワード制】へ変更となりました。` verbatim under the census's own `no-whitespace` fold (its finding 1687 already folded it). The `teaches` cell (ID/password gate with prior application since 2026-04-01) matches §注意事項/§事前申請【ID/PWの発行】 of the fetched page.

## Findings

1. **Extraction artifact flagged as payload-absent.** The census captured the single word `canonical` from inside a parenthetical `(… link rel="canonical")` note and scored it ABSENT against page text. Under the register's own rule (payload-absent = fabrication class), this row is not a fabrication: the asserted fact is verbatim-verifiable in the fetched HTML, and both intended quotes match.
2. **Id-namespace hazard.** Register `S129` is the round-3-namespace id (post-remap staged id S133). The staged package has a *different* row at S129 (`SOURCES.append.md:27`, the env-diff own-work row citing `tools/env-diff.py` + contract.json @ d16f9b5a), which is not what the register flags. A reviewer keying "S129" to the staged table would hand-check the wrong row.

## Residual risk / gaps

- Companion URLs and local artifacts claimed-checked by the register were not re-fetched; only the cited source was (sufficient for this verdict — the cited source alone carries the claim).
- Page is live Plone; content may drift. Fetched copy kept at `/tmp/tameshi-r40-ReviewQ129/ieice.html`.
- If adopted, the row's anchor text should cite the real quotes (boxed notice; ログインURL entry), not the parenthetical the census mangled.

## Disposition

Present. Correct the quarantined quote to the verified spans above; do not refuse the row.
