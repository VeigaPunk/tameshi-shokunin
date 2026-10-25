seat: ExecJudge03

C1 falsify wave (non-author re-judgment). Rows S078, S079, S156 — none authored by me
(entries authored by ExecRows13 / ExecRows14 / ExecRows24 respectively). Read-only on the lane
except this report; all scratch under `/tmp/tameshi-r45-ExecJudge03/`.

## Verdicts

S078 agree — reviewer ExecJudge03 — live open(2) bytes are byte-identical to the entry's raw_sha256 and to the committed snapshot (d665489c…); the 22-token quote sits at the O_TRUNC entry of the file-creation-flags list next to the FIFO/terminal-ignored and otherwise-unspecified sentences, and states an O_RDWR access mode allows writing and truncates a regular file, which is the row's teaches.
S079 agree — reviewer ExecJudge03 — live timezones page bytes are byte-identical to the entry's raw_sha256 and to the committed snapshot (382b3114…); the 17-token quote sits inside §"Avoid writing the current timezone" immediately before the TZ=UTC example and states TZ is the method when no dedicated option exists, the row's explicit-TZ teaches, with the section's own text supplying the other-timezone non-reproducibility counterexample.
S156 agree — reviewer ExecJudge03 — live PIT FAQ bytes are byte-identical to the entry's raw_sha256, to the committed snapshot and to the round-42 snapshot (ccf6ac49…); the 16-token quote is the §"Is it random?" two-factor caveat and the immediately following §Timeouts and §Static initializers sections name both factors and state a mutant may be timed out on one run but killed or surviving on another, matching the row's teaches.

Machine-readable copy for L1 integration: `/tmp/tameshi-r45-ExecJudge03/reviews.json`
(3 reviews, all `agree`, `reviewer":"ExecJudge03"`, `report":".ufo/waves/round-45/w2/ExecJudge03.md"`).

## Provenance (live vs ledger vs committed snapshot)

```
$ for spec in S078|https://man7.org/linux/man-pages/man2/open.2.html \
             S079|https://reproducible-builds.org/docs/timezones/ \
             S156|https://pitest.org/faq/; do id=${spec%%|*}; url=${spec#*|}; \
      curl -fsSL -A 'Mozilla/5.0' --max-time 90 -o "$id.live" "$url"; done
S078 curl_exit=0 bytes=76506
S079 curl_exit=0 bytes=40603
S156 curl_exit=0 bytes=20845

$ sha256sum S078.live S079.live S156.live
d665489cadb85624d98fae03a8d8d06209030f32735cff8aeba949ad8491c789  S078.live
382b311453d53b6a107c287abe33e59267fe883c4fb407d0bfe5854c894aaf65  S079.live
ccf6ac493d6935e2f0a90b716254c57024973d5e2bf1bf3c1e8e60b9772629c1  S156.live
```

| row | ledger raw_sha256 | live today | committed snapshot (ad5942c, gunzip -c | sha256sum) | equal |
|---|---|---|---|---|---|
| S078 | d665489cadb85624d98fae03a8d8d06209030f32735cff8aeba949ad8491c789 | d665489c…c789 | d665489c…c789 (blob 2ee6d0f98f0b4e5d464f373ac9a99ed9cccac61c) | yes, all three |
| S079 | 382b311453d53b6a107c287abe33e59267fe883c4fb407d0bfe5854c894aaf65 | 382b3114…af65 | 382b3114…af65 (blob 9a83c0edcd324b5ef1afa846d631de33fd606f7c) | yes, all three |
| S156 | ccf6ac493d6935e2f0a90b716254c57024973d5e2bf1bf3c1e8e60b9772629c1 | ccf6ac49…29c1 | ccf6ac49…29c1 (blob 75e47ad8d28f0733b079e85f0fe1e1496fa35984) | yes, all three |

Because the live bytes equal the ledger hash, the "dynamic page chrome" branch of the item
(re-extract today's live text and require the quote there) was not needed as a separate step —
the snapshot *is* today's live document. Committed-blob check:

```
$ git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show \
    ad5942c6e9858af19d00000b58439b321ddfa62b:.ufo/evidence/round-45/freshness/sources/S078.raw.gz | gunzip -c | sha256sum
d665489cadb85624d98fae03a8d8d06209030f32735cff8aeba949ad8491c789  -
(S079 → 382b3114…af65, S156 → ccf6ac49…29c1, same shape)
$ git status --porcelain -- .ufo/evidence/round-45/freshness/sources/S0{78,79}.raw.gz …/S156.raw.gz
(no output: worktree snapshots are the committed blobs)
```

S156's anchor cell cites `.ufo/evidence/round-42/sources/pit-faq.html 20845 B sha256 ccf6ac49`;
that file is present and hashes `ccf6ac493d6935e2f0a90b716254c57024973d5e2bf1bf3c1e8e60b9772629c1`
(`ls -l` 20845 B), so the author's "byte-identical to the round-42 snapshot" note is true.

## Located context (normalized `--extract` text of the committed snapshot; `[[…]]` = the quote)

```
$ python3 .ufo/evidence/round-45/freshness/measure.py --extract S078.snap   # 43578 chars, rc=0
... and ubifs (Linux 4.9) O_TRUNC If the file already exists and is
[[a regular file and the access mode allows writing (i.e., is O_RDWR or O_WRONLY ) it will be truncated to length 0.]]
If the file is a FIFO or terminal device file, the O_TRUNC flag is ignored. Otherwise, the effect of O_TRUNC is unspecified. creat() ...
```

```
$ python3 .ufo/evidence/round-45/freshness/measure.py --extract S079.snap   # 4109 chars, rc=0
Timezones ... Avoid writing the current timezone  Some tools will write date and time with the associated timezone:
$ LC_ALL = C date -d '@2147483647' --rfc-2822  Tue, 19 Jan 2038 04:14:07 +0100  Despite being given a pre-determined time ...
this output would fail to be reproducible in a different timezone than UTC+0100. The easy solution is to set the required
environment variable to force tools to use UTC as the timezone: $ LC_ALL = C date -u -d '@2147483647' --rfc-2822
Tue, 19 Jan 2038 03:14:07 +0000
[[When there is no dedicated option, it is most often possible to set the TZ environment variable:]]
$ TZ = UTC LC_ALL = C date -d '@2147483647' --rfc-2822 ... Note that both TZ=UTC and TZ=UTC0 styles are valid.
```

```
$ python3 .ufo/evidence/round-45/freshness/measure.py --extract S156.snap   # 11804 chars, rc=0
... Using the ALL option is strongly discouraged. Is it random? No. Given the same input Pitest will always generate
the same mutants, and (with a couple of caveats) will always produce the same results. Pitest works hard to be fully
deterministic, but [[two factors might cause the results to differ slightly between two runs with the same input]].
Timeouts Mutants causing infinite loops are detected by comparing the time taken to run a test without the mutant to the
time taken when the mutant is present. Both these measurements can be affected by external factors (other processes on
the machine etc), so a mutant may be detected as timed out on one run, but killed or surviving on another.
Static initializers As discussed above static initialization code ... can also result in small differences between runs,
especially if timeouts occur as these require starting a new jvm.
```

Each quote occurs exactly once in the normalized text (`t.count(quote)` = 1 for all three), is body
prose (not a `<title>`, nav/footer/cookie text, or a bare table/code fragment), sits at or next to the
row's anchor, and shares content words with the row's scope+anchor+teaches cells:

- S078 (22 tokens, within 6–25): shared `access, allows, file, mode, rdwr, regular, writing`
- S079 (17 tokens): shared `dedicated, option` — exactly the >= 2 threshold; the row's anchor names this
  paragraph ("paragraph before the TZ=UTC example") and the teaches' second clause (varying TZ as a
  reproducibility counterexample) is carried by the adjacent "would fail to be reproducible in a
  different timezone than UTC+0100" sentence, not contradicted by the quote.
- S156 (16 tokens): shared `between, differ, factors, input, results, runs`

None of the three quotes is a substring of its row's own source/scope/anchor/teaches cells
(`quote in cells` = False for all three), i.e. they were located afresh.

## Corroborating seat-helper run (never a deciding run)

```
$ python3 .ufo/evidence/round-45/freshness/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    --rev 3310e7be803516ca5934b4e949d91bcec824b179 --check /tmp/tameshi-r45-ExecJudge03/S078.json \
    --snapdir /tmp/tameshi-r45-ExecJudge03
CHECK S078 verified ok        rc=0
CHECK S079 verified ok        rc=0
CHECK S156 verified ok        rc=0
```

## Observations / risks (not disputes)

- S078 and S072 are two registry rows for the same URL, and their ledger quotes are byte-identical
  (`a regular file and the access mode allows writing …`). S078 is the supersede row, so the shared
  sentence is legitimate and each row still has its own committed snapshot blob and its own cells to
  match; I record it only so L1 knows the two rows are not independent *document* observations.
- `/tmp` is 100% full host-wide (`df -h /tmp` → `128G 128G 364K 100%`, later 787M free): the first
  `--check` attempt failed with `CHECK S### invalid snapshot absent` because `mkdir`/`cp` of the raw
  snapshot copy hit `No space left on device`. Worked around by hardlinking the already-gunzipped
  snapshots as `S078.raw`/`S079.raw`/`S156.raw` (metadata only). No lane state touched; this is an
  environment risk for any seat that needs a second copy of a snapshot.
- No tools installed or upgraded (pacman paused; nothing was needed — python3, curl, gunzip, sha256sum
  sufficed).
