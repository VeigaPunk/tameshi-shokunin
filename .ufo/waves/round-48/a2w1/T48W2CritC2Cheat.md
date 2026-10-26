# T48W2CritC2Cheat — cheapest pass on the frozen C2 counter

Attacked: claim C2 (freshness) and its frozen counter
`.ufo/evidence/round-48/freshness/measure.py` (sha256 `faefe9b442741bcd7238ffe028841a0da7453c14c70f9f33afbd0f77be2df63f`,
per `freeze-2.json`). I am not an author of the C2 records.

Scratch: clone `--shared` at base `473336d9d789f6081195e7376d17836a24666bc3`, toplevel
`/fast/scratch/hyaku/tameshi-r48/T48W2CritC2Cheat/lane`, throwaway identity used only there.
The frozen counter was copied byte-identically into the clone so `self_pin=1`, and every run used
`TMPDIR` under the scratch dir. The lane was never written except this report.

**Result: both constructions pass — `C2_R48_PASS=true` with live on, `refreshed=4` and
`C2_R48_PARTIAL=true` with `--no-live`, exit 0.** The cheapest construction contains **zero bytes
fetched from any source** (484 bytes of locally authored HTML). Nothing was re-opened this round.

---

## 1. Probe A — copies of old snapshots + forged receipts (the item's construction)

Material (all fabricated in the clone, no network):

| target | "round-48 snapshot" | source of the bytes | blob sha1 |
|---|---|---|---|
| S026 | `sources/S026.raw.gz` (41326 B) | `.ufo/evidence/round-45/freshness/sources/S026.raw.gz` | `d0b99641810341483beaca3a9de0aa82b50131d5` (identical) |
| S048 | `sources/S048.raw.gz` (3269 B) | `.ufo/evidence/round-45/freshness/sources/S048.raw.gz` | `f0f2ed1e8bcee781160287c575357b296acbf190` (identical) |
| S093 | `sources/S093.xml` (33289 B) | `.ufo/evidence/round-30/sources/S093-bwrap-0.13.1.xml` | `b48cf5b448270f2234da911cf24ba8b47469ee26` (identical) |
| S108 | `sources/S108.raw.gz` (17919 B) | `.ufo/evidence/round-45/freshness/sources/S108.raw.gz` | `9d31ce415b0b0171823006fc5591cdcf8ad5bef9` (identical) |

Also forged: four receipts (`fetched_at: 2026-10-26T11:07:00Z`, `http_status: 200`, `sha256` of
the copied bytes, `bytes` of the copied bytes); rows S265-S268 appended at
`corpus/SOURCES.md:139` in the 13-field shape, `teaches = "supersedes T — …"`, `opened
2026-10-26`, `status mined`, base URL in the source cell, digest prefix in the anchor cell; four
Gate lines in `corpus/lessons/round-48.md:3-6`; one `source:` append and one `verified-at:` date
bump per cited entry (nothing in the entries was re-read for content).

Run (lane counter, read-only; forged rev `49abb3cfbac45cc6ef9384158e1372e59e3e83f9`):

```
TARGET S026 row=S265 snapshot=ok receipt=ok quote=ok phrases=ok entries=ok live=ok REFRESHED
TARGET S048 row=S266 snapshot=ok receipt=ok quote=ok phrases=ok entries=ok live=ok REFRESHED
TARGET S093 row=S267 snapshot=ok receipt=ok quote=ok phrases=ok entries=ok live=ok REFRESHED
TARGET S108 row=S268 snapshot=ok receipt=ok quote=ok phrases=ok entries=ok live=ok REFRESHED
C2_R48: self_pin=1 targets=4 refreshed=4 census_exit=0 live=on rev=49abb3cf… C2_R48_PASS=true
EXIT=0
```

`--no-live` at the same rev: `refreshed=4 … C2_R48_PARTIAL=true`, exit 0.

The four quotes were lifted verbatim out of the copied snapshots' own extraction (S093's quote,
12 words, spans two `<varlistentry>` blocks — legal under amendment 2, which strips tags and
collapses whitespace, so a "sentence" that does not exist in the source becomes a quote).

## 2. Probe B — the cheapest construction (synthetic snapshots)

Replace the four copied blobs with four locally authored files that contain only the quote, e.g.
S048 is 81 bytes:

```
<html><body><p>it should therefore be prioritised above others</p></body></html>
```

Recompute the four digests, put them in the receipts and the anchor cells, commit
(`1c065dbd75b4550e8446bfb129078f05e8d401fa`). Same four rows, gate lines, entry edits.

```
--- no-live
TARGET S026 row=S265 snapshot=ok receipt=ok quote=ok phrases=ok entries=ok live=skipped REFRESHED
… (all four REFRESHED)
C2_R48: self_pin=1 targets=4 refreshed=4 census_exit=0 live=off rev=1c065dbd… C2_R48_PARTIAL=true
--- live
TARGET S026 row=S265 snapshot=ok receipt=ok quote=ok phrases=ok entries=ok live=ok REFRESHED
… (all four REFRESHED)
C2_R48: self_pin=1 targets=4 refreshed=4 census_exit=0 live=on rev=1c065dbd… C2_R48_PASS=true
EXIT=0
```

Cost of probe B: 484 bytes across four committed files, four hand-written receipts, four registry
rows, four lesson lines, eight one-line entry edits, one commit, ~2.3 s of counter time. Nothing
was fetched by the author; the only network traffic is the counter's own live check.

## 3. Why the live check does not catch it

Measured (one probe fetch per URL, the same fetch `check_live` performs):

| target | receipt sha256 (forged, over authored/copied snapshot) | live sha256 | live bytes | equal |
|---|---|---|---|---|
| S026 | `1bd8cc148336…`, 112 B | `dfea6b9ba734…` | 236387 | False |
| S048 | `13d27db2e1c3…`, 81 B | `e9cbc3e1ab7c…` | 8892 | False |
| S093 | `0b26ab9062b7…`, 123 B | `2cb77df2f4be…` | 33289 | False |
| S108 | `6dbea1197598…`, 168 B | `1b47b6efe5d8…` | 111409 | False |

`check_live` (`measure.py:336-350`) fetches the receipt URL and returns `ok` on
`quote in extract(raw)` alone (`measure.py:350`). It never compares the fetched bytes with the
snapshot or with the receipt. So the snapshot is decorative: the counter's own live bytes are
never used as evidence, only as proof that the URL is up and still contains a phrase that the
author copied from a previously fetched page.

In probe A the same blindness hides a real staleness: the round-45 S026 page bytes were
`5d74dd1c3c75…` (236387 B) and the live page is `dfea6b9ba734…` (236387 B) — different bytes, same
length, `live=ok`. S108: snapshot page `9056c530ca6c…`, live `1b47b6efe5d8…`, same length. Only
S048 (`e9cbc3e1ab7c…`) and S093 (`2cb77df2f4be…`, the immutable tag) are still byte-identical.

The receipt is lane-authored text and is graded as such: `check_receipt` (`measure.py:263-284`)
only asks that the URL is in the row's own URL set (`:274`), that `fetched_at` starts with
`2026-10-26` (`:276`), that `http_status` is the string `200` (`:278`), that `sha256` equals the
digest of the *snapshot* (`:280`), and that a `bytes` key exists (`:282`) — its value is never
compared to anything. The anchor cell is likewise lane text: `check_snapshot` only requires the
computed digest's 12-hex prefix to occur somewhere in it (`measure.py:251-253`), so a fabricated
snapshot's own digest is written into the lane's own anchor as "fetched 2026-10-26".

This is the same defect class round-48 closed for C1: amendment 4 demoted lane-authored
observation receipts to "evidence for the report only, never attestation" and required
in-invocation observation. C2 kept a lane-authored receipt as the attestation of its only
sourced axis.

## 4. What must catch it

Smallest safe correction (counter, before the claim is scored):

1. `check_live`, after the fetch: require `sha256_hex(raw) == digest` and
   `str(len(raw)) == str(data.get('bytes'))` before returning `ok`; print `sha` / `bytes` (or a
   `stale` state) otherwise. With this, probe B fails 4/4 and probe A fails S026 and S108.
2. Define the snapshot digest over the fetched representation. `.gz` snapshots make this
   impossible today: `check_snapshot` digests the compressed bytes (`measure.py:251`) while
   `check_live` sees the decompressed response; the two can never be bound. Either commit
   snapshots uncompressed (as the genuine records do) or declare the encoding in the receipt and
   compare decompressed digests.
3. Predicate amendment, mirroring amendment 4: the receipt is not evidence; only bytes the
   counter itself fetched in the same invocation attest `refreshed`. A committed receipt must be
   demoted to report-only, and the label must carry e.g. `live_sha=4`.
4. Non-author re-open: reproduce the receipt's `sha256` from `curl -fsSL "$url" | sha256sum` and
   diff it against the committed snapshot; the probe above (receipt `1bd8cc…` vs live
   `dfea6b9b…`) is what that check sees. A blob-identity check (`git rev-parse
   REV:path` against the round-45/round-30 paths) shows the copy even when the live bytes happen
   to match.

## 5. Residual tradeoff (not a defect the correction can close)

Even with digest equality, a copied snapshot of an upstream that has not changed since an earlier
round passes: S048's page is byte-identical since 2026-10-20 and S093's is the immutable tag
`v0.13.1` from round 30. No counter can prove when bytes were obtained; only a counter-performed
fetch written into the receipts-only commit (in-invocation attestation) removes the human step.
The canonical judge must decide whether "re-anchored to unchanged bytes" is a legal outcome (then
the freshness increment for those targets is nil and should be reported as such) or whether the
claim needs counter-written snapshots. What is *not* a tradeoff is probe B: a 484-byte authored
file cannot be a fetch, and the frozen predicate credits it.

## 6. Impacted axes

- freshness (C2): the target `refreshed=4` / `C2_R48_PASS=true` is reachable at zero cost, so the
  claim cannot measure the freshness step it claims; any PASS from this counter is uninformative
  without an independent provenance check.
- calibration (C1's axis), as the pattern: C1 was fixed for exactly this (amendment 4), C2 was not;
  the round thus measures attestation discipline on one axis and abandons it on the other.

## 7. Secondary observation

Amendment 2 makes cross-element quotes legal by construction: S093's 12-word quote reads
"--unshare-cgroup-try Create a new cgroup namespace if possible else skip it --unshare-all",
spanning two `<varlistentry>` blocks. This is used by the genuine record too, so it is the
amendment's choice, not an author error; it does mean a Gate "quote" need not be a sentence the
source contains, which weakens the "located" claim. Also: the round-45 S093 blob-page snapshot
extraction contains escaped markup tokens (117-word span between the two required phrases), so it
cannot carry a single <=25-word two-phrase quote — the copy route for S093 has to use the round-30
raw XML (as probe A did).

## 8. Reproduction

```
S=/fast/scratch/hyaku/tameshi-r48/T48W2CritC2Cheat; mkdir -p "$S"; export TMPDIR="$S"
git clone -q --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin "$S/lane"
git -C "$S/lane" rev-parse --show-toplevel   # => $S/lane
git -C "$S/lane" checkout -q -B cheat 473336d9d789f6081195e7376d17836a24666bc3
# write measure.py (frozen bytes), sources/, receipts, rows at SOURCES.md:139,
# corpus/lessons/round-48.md, entry source:/verified-at: lines; commit with a throwaway identity
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-48/freshness/measure.py \
  --lane "$S/lane" --rev <rev>            # C2_R48_PASS=true
python3 …/measure.py --lane "$S/lane" --rev <rev> --no-live   # refreshed=4, C2_R48_PARTIAL=true
```

Tooling: nothing installed or upgraded. Scratch dir `/fast/scratch/hyaku/tameshi-r48/T48W2CritC2Cheat`
deleted after this report; disk guard not needed (peak use under 200 MB, `/fast` 622 G free).
