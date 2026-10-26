# T48W2ExecC2Run — frozen C2 counter executed at CONTENT

Seat: executor, wave a2w1. Item: run the frozen C2 (freshness) counter at CONTENT into scratch in
three modes, plus the site census, and paste every TARGET line, final line and every E/W line
naming S265-S268. Read-only on the lane; the only lane writes are this file and
`.ufo/waves/round-48/a2w1/T48W2ExecC2Run-census.out.txt`.

What this attacks: the C2 claim's own instrument — that `C2_R48_PASS=true` is reproducible from a
seat invocation at the content revision (not only inside the L1's virtualenv, worktree or receipt
files), that the counter separates CONTENT from the do-nothing base, and that the census the
predicate depends on (`census_exit=0`) is really 0 with the four new rows in place.

## Frozen identity (checked before running)

    $ sha256sum .ufo/evidence/round-48/freshness/measure.py
    faefe9b442741bcd7238ffe028841a0da7453c14c70f9f33afbd0f77be2df63f

Matches `freeze-2.json` → `counters["freshness/measure.py"].sha256` exactly (byte-identical to the
wave-1 counter, `changes: "none"`). `statements.json` also matches
`924102dfbc6135a7d9dabef7b8b2e681a5ce4c42ca72a031ea1f8d5ab9fb2e56`.

CONTENT `c7586b9a10effc63b4bd327f976edc094c1bdc17` exists and is an ancestor of lane HEAD
`17cc5ce1`; `git diff --stat CONTENT..HEAD` shows only the four a2w1 dispatch files
(`spec-a2w1.json`, `a2w1-dispatch.{json,err}`, `a2w1.ready`), so CONTENT's corpus/evidence bytes are
what HEAD serves. The lane worktree stayed clean throughout my runs (`git status --porcelain` =
only `?? .ufo/waves/round-48/a2w1/`, my own report dir).

## R1 — selftest

    $ TMPDIR=$S python3 .ufo/evidence/round-48/freshness/measure.py --selftest
    …
    SELFTEST 40_census_nonzero: PASS
    SELFTEST 41_live_absent: PASS
    SELFTEST 42_live_unreachable: PASS
    SELFTEST 43_no_live_partial: PASS
    C2_R48_SELFTEST: cases=43 failed=0
    exit 0

43 cases / 0 failed, identical to the freeze-2 record. The three cases that matter for a live
deciding run are present and green: `41_live_absent` (fresh bytes without the quote → `live=absent`
→ NOT refreshed), `42_live_unreachable` (network failure → `live=unreachable` → NOT refreshed, i.e.
"unreachable is reported, never credited"), `43_no_live_partial` (the `--no-live` label is PARTIAL,
never PASS).

## R2 — CONTENT, `--no-live`

    $ TMPDIR=$S python3 .ufo/evidence/round-48/freshness/measure.py \
        --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
        --rev c7586b9a10effc63b4bd327f976edc094c1bdc17 --no-live
    TARGET S026 row=S265 snapshot=ok receipt=ok quote=ok phrases=ok entries=ok live=skipped REFRESHED
    TARGET S048 row=S266 snapshot=ok receipt=ok quote=ok phrases=ok entries=ok live=skipped REFRESHED
    TARGET S093 row=S267 snapshot=ok receipt=ok quote=ok phrases=ok entries=ok live=skipped REFRESHED
    TARGET S108 row=S268 snapshot=ok receipt=ok quote=ok phrases=ok entries=ok live=skipped REFRESHED
    C2_R48: self_pin=1 targets=4 refreshed=4 census_exit=0 live=off rev=c7586b9a10effc63b4bd327f976edc094c1bdc17 C2_R48_PARTIAL=true
    exit 0

## R3 — CONTENT, live on (the mode the deciding run uses)

    $ TMPDIR=$S python3 .ufo/evidence/round-48/freshness/measure.py \
        --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
        --rev c7586b9a10effc63b4bd327f976edc094c1bdc17
    TARGET S026 row=S265 snapshot=ok receipt=ok quote=ok phrases=ok entries=ok live=ok REFRESHED
    TARGET S048 row=S266 snapshot=ok receipt=ok quote=ok phrases=ok entries=ok live=ok REFRESHED
    TARGET S093 row=S267 snapshot=ok receipt=ok quote=ok phrases=ok entries=ok live=ok REFRESHED
    TARGET S108 row=S268 snapshot=ok receipt=ok quote=ok phrases=ok entries=ok live=ok REFRESHED
    C2_R48: self_pin=1 targets=4 refreshed=4 census_exit=0 live=on rev=c7586b9a10effc63b4bd327f976edc094c1bdc17 C2_R48_PASS=true
    exit 0

**No target is NOT REFRESHED, so this item has no failing-check finding.** Every check field is
`ok` for all four targets and the label is the claim's target `C2_R48_PASS=true`.

`live=ok` is not a tautology of the receipt: `check_live`
(`.ufo/evidence/round-48/freshness/measure.py:336-349`) re-fetches the receipt's URL over the
network in this invocation and returns `ok` only when the Gate quote is a substring of the freshly
fetched extracted text; any exception becomes `unreachable`. Four distinct URLs were fetched (the
per-invocation cache at `:408` is keyed by URL, so S048's repeated PIT URL is one fetch, not four).

## R4 — do-nothing control probe (base, `--no-live`), separation evidence

    $ … --rev 473336d9d789f6081195e7376d17836a24666bc3 --no-live
    TARGET S026 row=none snapshot=- receipt=- quote=- phrases=- entries=- live=skipped NOT
    TARGET S048 row=none snapshot=- receipt=- quote=- phrases=- entries=- live=skipped NOT
    TARGET S093 row=none snapshot=- receipt=- quote=- phrases=- entries=- live=skipped NOT
    TARGET S108 row=none snapshot=- receipt=- quote=- phrases=- entries=- live=skipped NOT
    C2_R48: self_pin=0 targets=4 refreshed=0 census_exit=0 live=off rev=473336d9d789f6081195e7376d17836a24666bc3 C2_R48_PARTIAL=false
    exit 1

This is CTL_F's shape observed by a seat, not a control receipt: at base the counter finds no
superseding row (`row=none`) and scores `refreshed=0`, false. (`self_pin=0` at base is correct and
not a defect: `SELF_PATH` has no blob at the base revision, so the pin cannot match —
`measure.py:402`.) The counter therefore does not pass vacuously.

## R5 — site census

    $ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
    CENSUS_EXIT=0

16 output lines, no `E` line at all. Full capture:
`.ufo/waves/round-48/a2w1/T48W2ExecC2Run-census.out.txt`. Every E/W line naming S265-S268 (all four
are `W`, none `E`):

    tameshi	W04	S265 duplicate url testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html across scopes
    tameshi	W04	S266 duplicate url pitest.org/quickstart/incremental_analysis across scopes
    tameshi	W04	S267 duplicate url github.com/containers/bubblewrap/blob/v0.13.1/bwrap.xml across scopes
    tameshi	W04	S268 duplicate url www.tensorflow.org/federated/golden_tests?hl=zh-cn across scopes

## Observations (disclosures, not predicate failures)

1. The four `W04` lines are structural and expected. `W04` is printed when a URL was already seen
   and this `(url, scope)` pair is new (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh:645`),
   and the census header states warnings do not affect clean lanes (`:33`, `:36`). The held rows
   S026/S048/S093/S108 keep their URLs (C2 requires "source cell carries T's URL") while the new
   rows carry different scope text — S026 "Post body, published 2016-05-27 (fetched 2026-10-19)" vs
   S265 "Post body (h2 title; publishdate 2016-05-27; …)", and likewise for S266/S267/S268. That
   divergence is what avoids `E04` (which also needs a missing `supersedes S…` teaches clause);
   it costs one `W04` per new row. This class pre-exists at base (S047/S048, S075-S078, S081, S092,
   S104, S160 → 10 of the 14 `W04` lines), so round 48 adds exactly four.
2. The `--root … tameshi` invocation I ran reads the worktree, while the counter's own
   `census_exit` grades a materialised tree written from the REV blobs
   (`_materialise`, `measure.py:356-380`) and passes `--file`. Both are 0 here; I note the
   difference only so the L1 does not read my site census as "the counter ran this exact command".
3. `live=ok` means "the quote is located in the bytes fetched now", not "the bytes fetched now hash
   to the receipt's sha256". Snapshot/receipt equality is enforced separately
   (`check_receipt`, `measure.py:275-297`, `sha256` vs the snapshot digest) and the anchor cell
   carries the snapshot's 12-hex prefix (`check_snapshot`, `:245-247`). I re-derived the four
   digests independently from the CONTENT blobs and all four prefixes appear in the anchor cells:
   S026.html `a4c5c46b4af9`, S048.html `e9cbc3e1ab7c`, S093.xml `2cb77df2f4be`, S108.html
   `04e4c091715a` — matching the receipts' `sha256`/`bytes` (`200`, `fetched_at`
   2026-10-26T08:40:42Z–08:41:18Z).
4. Gate-line word counts from CONTENT `corpus/lessons/round-48.md` (limit 25): S265→S026 15 words,
   S266→S048 21, S267→S093 25, S268→S108 6. All within limit; S267 is exactly at it, so any editor
   touching that quote must not grow it.
5. Amendment 8 tension, disclosed. I ran the C2 counter at the content revision three times
   (selftest, `--no-live`, live) because this item instructs exactly that. None of these is a
   "deciding invocation" in the amendment-8 sense: no receipt under `.ufo/evidence/round-48/after/`
   was written, nothing was committed, and the frozen counter is a read-only grader of REV blobs
   apart from the network GET in `live`. If the L1 reads "a second deciding invocation at the
   content revision is a miss" as covering seat probes with `live` on, that reading would void the
   item it wrote; flagging it rather than deciding it.

## Cleanup / tooling

Scratch `S=/fast/scratch/hyaku/tameshi-r48/T48W2ExecC2Run` held only `census.out` (copied into the
deliverable dir above, byte-for-byte) and the counter's own `tempfile.mkdtemp` work dirs, which the
counter removes in `finally`. Scratch dir deleted; nothing left under
`/fast/scratch/hyaku/tameshi-r48/T48W2ExecC2Run`. `/tmp` was never used (`TMPDIR=$S` on every
run). Disk guard showed 620.4G free before the pass.

No tool installed or upgraded (pacman is paused host-wide; nothing was needed).
