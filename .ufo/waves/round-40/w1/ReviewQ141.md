# ReviewQ141 — quarantined S141: is an 86-site census in commit `31687496`?

**Verdict: NO. `payload-absent` confirmed.** Commit `31687496b5f34b153626e123d12ae2febdbd86a0` contains no 86-site writeFileSync census — not in its diff, not anywhere in its tree.

## Command and output

`git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 31687496`

- Subject: `round-35: final before + v2 control receipts on the 9-copy panel (before exit 1; control 0/6 kill 0/3 accept exit 1) + tool selftest 33/33 under the final pins`.
- Diff touches exactly **2 files, 36 insertions, 1 deletion**:
  - `.ufo/evidence/round-35/control/c1-v2-control.stdout` (+2/−1 — one added `COPY kill root-keyed-shape6` row; summary line re-spun `pub_slots=9 pub_distinct=9 … rev=691bb512…`)
  - `.ufo/evidence/round-35/lessons/selftest-33.out` (new; 33 `CASE … PASS` lines + `TALLY_AUDIT_V3_SELFTEST: 33/33 pass`)
- `git show 31687496 | grep -nE '86|site|census'` → only hash-substring matches (`b5f34b153626e123d12ae2febdbd86a0`, `7b11ba25aead9367`); no census content.

## Why the anchor cannot carry the claim even at the tree level

S141's corrected row (`/home/vgpnk/Projects/shokuknow/lanes/tameshi/round5/SOURCES-PROPOSED.md:21`, staged id S141 per round-39 `dispatch-w1.json:60`) anchors: "the six pinned blobs `kumitate-shokunin/scripts/{kimi-census,claims-check,round-gate,cite-check,proxy-check,surface-probe}.mjs` … read with `git show`, @ revision 31687496", teaching **86 `writeFileSync` sites**.

- `kumitate-shokunin` is a *sibling* repo (`/home/vgpnk/Projects/shokunin/kumitate-shokunin`), not a path in tameshi: `git ls-tree 31687496` shows no `kumitate-shokunin/` tree — a tameshi rev cannot pin those blobs by `git show` at all.
- The rev only carries *embedded copies* of 4 of the 6 named gates, as JSON `files.<name>.source` in `.ufo/evidence/round-25/mte-reports/*.mte.json`. Counted directly at the rev:
  - `js-kimi-census.mjs` 15 · `js-claims-check.mjs` 5 · `js-round-gate.mjs` 17 · `js-sources-check.mjs` 6 → **43 `writeFileSync` total** (sources-check is not even one of the six named).
  - `cite-check` exists only as round-26 sweep artifacts (no embedded source); `proxy-check`/`surface-probe` have no pinned blob in the tree.
- So even granting the embedded copies as "the pins": **43 ≠ 86**, and 4-of-6 gates pinned ≠ six pinned blobs. No honest rerun over this rev's pins yields 86.

## Corroborating dispositions (same class, already recorded)

- `corpus/lessons/round-39.md:28` — Reject: "S141 cites the same revision `31687496` for an 86-site census that is not in that commit. `payload-absent`, not a fetch failure."
- `LOG.md:2067` — "Staged S137 and S141 refused (payload-absent at `31687496`)."
- `.ufo/waves/round-39/w1/ScoutQ141.md` — the four-gate predecessor row also falsified; no six-gate pin set exists at this rev.

## Residual risk / gaps

- The round-5 row could only be resurrected by pinning the six blobs in the *kumitate* repo at a rev that actually yields 86 `writeFileSync` sites — a different commit than `31687496`. As written, falsified.
- No tools installed; read-only `git show/ls-tree/grep` on the lane plus shokuknow reads only. No lane, index, or shokuknow mutation.
