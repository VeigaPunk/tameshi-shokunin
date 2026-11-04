# tameshi round 73 — lesson

Round 73 (attempt 1), base `a3dd35742eee608d1205843dacebc461b4242b9e`
(`= origin/master`, clean tree — the round-72 non-author verifier spot-check
commit). Claims, counters, kill rules, arms and controls are frozen **before
any claim data** in `plans/round-73.plan.md` (declaration commit). Round
shape: one v1 wave, 13 seats (3 executor · 2 scribe · scout · 2 reviewer ·
critic · mutation-tester · sentinel · revenger · connector), policy band
8–16. `labrat` is a frozen-topology seat the validator rejects
(`~/Projects/ufo-fsd-alpha/scripts/ufo-swarm-wave.mjs:263`), so no labrat item
exists — the round-72 defect this round pays was a plan that declared one
anyway.

## Declared claims (frozen pre-data)

- **R73-C1 — calibration (the lowest scored numeric axis at 8; capability
  acquisition; sourced on the re-opened S066).** `tools/wave-reconcile.py` +
  `tools/wave-reconcile.json` (schema `tameshi-wave-reconcile-v1`): a round
  record's execution claims — seat count, committed seat-report count, role
  multiset, attack share — are re-derivable from the committed wave artifacts.
  Rows bind a record span by byte substring at the record revision with the
  printed integer a delimited token; artifacts are read from git objects at
  their own revision; `expect: meet|drift` so a standing red arm MEASURES the
  drift on every sweep; a UTF-8 BOM is a setup exit 2, never silently
  stripped. Standing manifest: six rows over the committed round-72 wave —
  four green and the round-72 closure's two routed defects as red arms.
- **R73-C2 — operability (verdict-only).** `tools/rekey-cost.py --arms`
  turns the recorded rekey-cost arm table into a re-runnable 7-arm battery
  and adds the ignored-path arm the round-72 wave's coverage finding named.
  Frozen outputs: `REKEY_ARMS: arms=7 meet=7 unexpected=0` exit 0, selftest
  unchanged 8/8, and the same battery under the IGNORED-filter mutant M3
  reads `unexpected=1` naming `ignored-skill`.

## Carry-in from the round-72 non-author closure

`corpus/lessons/round-72-verifier-spotcheck.md` (admitted; five status-neutral
routed defects, two carries). Dispositions declared pre-data in
`plans/round-73.plan.md`: defects 1 and 2 become C1's two measured red arms;
defect 3 is restated in this lesson's `## Gate`; defect 4 corrects the
pointer-recheck manifest's note count; defect 5 is paid in this round's LOG
entry (the three receipt-only commits of round 72 are named there as
inheriting the "Round 72 — appended after the wave" entry); carry 6 is C2;
carry 7 (inherited record misses) is re-measured at the tip and reported as
inherited.

## Gate — the source (S066 re-opened this round)

**Re-open, not a new row.** RFC 8259 is already held as S066 for a different
section (§6 number grammar). This round's instrument rests on §8.1's encoding
ground, so a new row on the same URL would be a within-scope duplicate
(CORPUS.md rule 2; the S289/S293 standing rejection, re-sampled by the
round-72 closure). The curation delta is therefore a **re-open**: S066's
`used-by` cell gains `corpus/lessons/round-73.md` and this Gate carries the
fresh located quotes.

- Source: RFC 8259, *The JavaScript Object Notation (JSON) Data Interchange
  Format* (T. Bray, Ed.), <https://www.rfc-editor.org/rfc/rfc8259>, text form
  <https://www.rfc-editor.org/rfc/rfc8259.txt>. Fetched 2026-11-04 (HTTP date
  `Wed, 04 Nov 2026 00:58:08 GMT`; 28,360 B; sha256
  `61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7`;
  extract `.ufo/evidence/round-73/sources/rfc8259.txt`, headers
  `.ufo/evidence/round-73/sources/rfc8259-headers.txt`).
- Quote 1 (§8.1 Character Encoding, page lines 485–486, 18 words): "JSON
  text exchanged between systems that are not part of a closed ecosystem MUST
  be encoded using UTF-8" — the encoding of record for the artifacts the
  instrument parses.
- Quote 2 (§8.1, page lines 494–495, 17 words): "Implementations MUST NOT add
  a byte order mark (U+FEFF) to the beginning of a networked-transmitted JSON
  text."
- Quote 3 (§8.1, page lines 496–498, 21 words): "implementations that parse
  JSON texts MAY ignore the presence of a byte order mark rather than
  treating it as an error" — the RFC permits either; this lane chooses the
  fail-closed arm (a named setup exit 2) because silently stripping bytes the
  emitter was told not to add would let a rewritten artifact masquerade as
  clean (the round-72 EOL defect's class, made visible instead of invisible).
- **Admit:** S066's §8.1 re-open (the two normative sentences plus the
  permitted-alternative sentence above; the §6 number-grammar scope is
  unchanged and stays as written).
- **Reject (standing, re-sampled):** a new RFC 8259 row for the §8.1 ground —
  same URL, same document, within-scope duplicate; flip condition: the §6
  scope is retired or the document is superseded by a new RFC, at which point
  the successor is a new document with a new row.

## Gate — the census sentence (round-72 closure defect 3, restated)

The round-72 report's sentence "the counter-run without the prefix prints
E04" is true only of a **same-scope fixture**: on the real registry a
superseding row with a restated scope prints `W04 duplicate url … across
scopes` and the lane still validates clean. Measured this round on the live
registry (`scripts/sources-census.sh validate --root <fleet> tameshi`): the
S303 row prints W04, exit 0. The correction of record is this paragraph; the
round-72 report is append-only history and stands as written.

## What was measured

Pending: the counters land at the round's work and receipts commits (the
measured sections are appended below, never rewritten).
