# T55W1ScoutReceipts — round-54 spotcheck receipt inventory

Seat: T55W1ScoutReceipts. Axis: calibration. Milestone: receipt inventory.
Rev checked: `0a2010acd1e92e4e332774050825e21bcfc7e079` (lane `tameshi-shokunin`).
Spotcheck: `corpus/lessons/round-54-verifier-spotcheck.md` at that rev, blob, 26054 bytes, sha256 `642fedd514a6c20372cd299940adb2e0041f651288c6f4ae6d8530f6b612917d`. Worktree bytes match the blob.

Method: `git cat-file` / `git show <rev>:<path>` / `git grep` at that rev only. No lane production file was edited. No tool was installed. Command output: `.ufo/waves/round-55/w1/T55W1ScoutReceipts-receipts/inventory.json` (and `empty-blobs.txt`, `s277-*.txt`, `s279-*.txt`).

"Quoted line present = yes" means every concrete token of the spotcheck's quote is on that line in order. An ellipsis in the spotcheck is the author's abbreviation, not a required byte. A quote that is not a substring of the cited object is `no`.

## Sweep

Every receipt the spotcheck says is in the tree exists at this rev, is a blob, and is non-empty. None of the cited paths is missing.

`git ls-tree -r -l <rev> -- .ufo/evidence/round-54` finds one empty blob: `.ufo/evidence/round-54/after/census.stderr` (0 bytes, oid `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391`). The spotcheck does not name that path. Not a missing-receipt finding.

The old forged path `.ufo/waves/round-54/w2/T54W2Sent01-forged-reader.json` is absent. The spotcheck says `7fa9a5e` renamed it. Absence confirms the claim.

`w1-results.json` and `w2-results.json` are absent. The spotcheck says they are absent. `w1.ready.dispatched` (2657 bytes) and `w2.ready.dispatched` (1463 bytes) are present blobs. No line is quoted from them.

## Table (R54.1–R54.10)

| R-id | receipt at `0a2010ac` | blob, non-empty | quoted line present | line |
|---|---|---|---|---|
| R54.1 | `.ufo/evidence/round-54/control/controls-b.stdout` | blob 654 | yes | 1 |
| R54.1 | same | blob 654 | yes | 2 |
| R54.1 | same | blob 654 | yes | 5 |
| R54.1 | `.ufo/evidence/round-54/control/controls-b.exit` | blob 104 | yes (digit `1`; the words `exit 1` are not in the file) | 1 |
| R54.2 | `.ufo/evidence/round-54/after/frozen.stdout` | blob 112 | yes (`freeze=077d431e` is the prefix of the 40-hex token) | 1 |
| R54.2 | `.ufo/evidence/round-54/freeze.json` | blob 3266 | yes, derived (`len(amendments)=5`, 10 files). The literal `5 amendments` is not a line | amendments key |
| R54.3 | `.ufo/evidence/round-54/before/c2.stdout` | blob 1307 | yes (`total=13`) | 8 |
| R54.3 | `.ufo/evidence/round-54/contract.json` | blob 5489 | yes (`total=13` in `C2.before`) | 28 |
| R54.3 | `.ufo/evidence/round-54/**` | n/a (grep) | yes that `total=14` is absent (`git grep` rc 1) | — |
| R54.4 | `.ufo/evidence/round-54/freeze.json` | blob 3266 | yes (`8528ee85…` on `c2/measure.py`) | 9 |
| R54.4 | same | blob 3266 | yes (`d7749f84…` on `c1/measure.py`) | 8 |
| R54.4 | same | blob 3266 | yes that `49280fe5` is absent | — |
| R54.4 | `19c7558` and `7e533b1` `c2/measure.py` | historical blobs, not paths at this rev | yes (sha256 `49280fe55bd9361c…`, 9375 bytes, regex `mkdir(?:at)\(`) | — |
| R54.5 | `.ufo/waves/round-54/w1/*Read*.json` | 23 blobs | yes, derived: 28 findings, 28 distinct JSON objects, 15 files with findings | — |
| R54.5 | `.ufo/waves/round-54/w2/*Read*.json` | 23 blobs | yes, derived: 25 findings in 12 files (11 files have 0) | — |
| R54.5 | `.ufo/evidence/round-54/integrate/resolutions.json` | blob 8713 | yes, derived: 12 entries, 25 findings | — |
| R54.5 | `.ufo/evidence/round-21/coldread/ledger.json` | blob 10572761 | yes, derived: 591 entries; 23 whose `traces` name `rekey-r54-99c3bc88d704`; all `verdict=gap-minor`, all `read_rev=99c3bc88d704566197783f66b211ee0a830e0330`; `minor_gaps` histogram `{0:11, 1:8, 2:3, 11:1}` | — |
| R54.6 | `.ufo/evidence/round-54/after/clean-tree-after.txt` | blob 222 | yes | 2, 3, 4 |
| R54.6 | `.ufo/waves/round-54/w2/T54W2Sent03.md` | blob 15851 | yes (object exists; no quote to match) | — |
| R54.6 | `.ufo/waves/round-54/w2/T54W2Sent03-receipts/c1committed-positive.stdout` | blob 362 | yes (exists) | — |
| R54.6 | `.ufo/waves/round-54/w2/T54W2Sent03-receipts/rejection-attribution.txt` | blob 1253 | yes (exists) | — |
| R54.7 | `.ufo/waves/round-54/w2/T54W2Sent01-receipts/forged-reader.json` | blob 187 | yes | 1 |
| R54.7 | `.ufo/waves/round-54/w2/T54W2Sent01-forged-reader.json` | absent | yes (absence is the claim) | — |
| R54.7 | `.ufo/waves/round-54/w2/T54W2Read01.json` (genuine reader; spotcheck does not name this path) | blob | yes (`61736dce…`) | 1 |
| R54.8 | `.ufo/waves/round-54/w1/T54W1ExecStraceNoise.md` | blob 19216 | **no** at the cited line | 324 |
| R54.8 | same | blob 19216 | yes only after joining the wrap | 325–326 |
| R54.8 | `~/.omp/agent/config.yml` | not a lane blob | yes on the live host file this run (`scout: "@m_grok"`). Not pinned by the rev | 418 |
| R54.9 | `.ufo/waves/round-54/w1-registry.json` | blob 1938 | yes (`seats` 76, `attack_seats` 21, `reviewer` 5, role_mix sums to 76) | 7, 8, 10–19 |
| R54.9 | `/home/vgpnk/Projects/shokuknow/merge/tameshi/knowledge` | not a lane blob | yes, derived: 81 `*.md` via `os.walk` this run | — |
| R54.10 | `.ufo/evidence/round-54/control/controls-a.stdout` | blob 853 | yes (`CTL CTL_R53` prints `rekeyed=0/7`, not `rekeyed=0/30`) | 3 |
| R54.10 | `.ufo/evidence/round-54/control/r53-counter-at-88afa941.stdout` | blob 3019 | yes (`rekeyed=0/30`) | 1 |

Historical freeze.json counts the spotcheck states, checked at those commits (not blobs of this rev's tree): `7883e0e5` is 7 files / 1 amendment; `fe70474` is 10 files / 4 amendments; `097985c` is 10 files / 2 amendments. The parentheticals match. `fe70474`'s `c2/measure.py` pin is already `8528ee85`.

## Exact lines

R54.1 `.ufo/evidence/round-54/control/controls-b.stdout:1`

```
CTL CTL_POS_c1 C1_R54: rev=077d431e6996 c0=99c3bc88d704 credited=60 lost=4 rekeyed=3/7 readers=6/7 monitor=6/60 unstable=0 total=4 C1_R54_PASS=false
```

`:2` `CTL_MISMATCH CTL_POS_c1 expected=true actual=false`
`:5` `CONTROLS_B: 2/3 as pre-registered`
`controls-b.exit:1` `1`

R54.2 `.ufo/evidence/round-54/after/frozen.stdout:1`

```
FROZEN_UNCHANGED=1 freeze=077d431e69965fa4673cd006ab64f6fc387f9e15 rev=c21081008adbb6b6fe4e58a0aeec4831b30e318c
```

`5 amendments` is not on that line. `freeze.json` has an `amendments` array of length 5.

R54.3 `.ufo/evidence/round-54/before/c2.stdout:8`

```
C2_R54: rev=d33053f7552d tools=7 unusable_exit2=3 naming=7 empty_ok=7 usable_ok=7 tmp_mkdirs=0 docs=0 note=0 sources=0 total=13 C2_R54_PASS=false
```

R54.4 `freeze.json:9` pins `c2/measure.py` = `8528ee8555da068519af4159f5f9e0efac8b29de88a53534a7043d7ec007e790`. `:8` pins `c1/measure.py` = `d7749f8469fbd49b4daaca6eacef89bc1cf48f553702b4f2fe1a7c80d5245812`.

R54.6 `.ufo/evidence/round-54/after/clean-tree-after.txt`

```
?? .ufo/evidence/round-54/after/
?? .ufo/waves/round-54/w2/T54W2Sent03-receipts/c1committed-positive.stdout
?? .ufo/waves/round-54/w2/T54W2Sent03-receipts/rejection-attribution.txt
?? .ufo/waves/round-54/w2/T54W2Sent03.md
```

The three seat paths are lines 2–4. Line 1 is a fourth `??` the spotcheck does not mention.

R54.7 forged receipt, one line, `section_sha256` `b90c1f799d0ce42a9fbb04b156ce9d5b4bb7395235b2fc9ca4b426669feb9927`. Genuine reader `T54W2Read01.json:1` has `61736dcebc2d3d148255f9b3edd0ceb1c7cf2284f2969475b8da838ded9a78fc`. Section re-hash at c0 was not redone here.

R54.8 cited line 324 is not the quote:

```
Scope note: `~/.omp/agent/config.yml` is outside this seat's default write scope (the wave `w1/`
```

Lines 325–326, joined, do contain `on the operator's direct instruction in-session, which is the higher authority` (`higher` / `authority` are split by the newline).

R54.9 `w1-registry.json`: `"seats": 76` (line 7), `"attack_seats": 21` (line 8), `"reviewer": 5` (line 16). role_mix is scribe 27, executor 13, scout 4, connector 2, mutation-tester 12, critic 4, reviewer 5, sentinel 4, revenger 3, simplifier 2.

R54.10 `controls-a.stdout:3`

```
CTL CTL_R53 C1_R54: rev=88afa9415454 c0=none credited=58 lost=6 rekeyed=0/7 readers=0/7 monitor=6/58 unstable=0 total=4 C1_R54_PASS=false
```

`r53-counter-at-88afa941.stdout:1`

```
C1_R53: rev=88afa9415454 credited=58 lost=6 rekeyed=0/30 readers=25/30 total=37 C1_R53_PASS=false
```

The fleet report `.ufo/reports/round-54/tameshi.md:50-52` (fleet HEAD, not a lane blob at this rev) does quote `` `CTL_R53` (the round-53 final tree, 58/64, `rekeyed=0/30`) `` under `control/controls-a.stdout`. That quote is not in the receipt. `58/64` matches this line's `credited=58 lost=6` (58+6=64); `rekeyed=0/30` does not.

## Other receipts the spotcheck cites

| id | path | blob, non-empty | quoted line present | line |
|---|---|---|---|---|
| C1 | `.ufo/evidence/round-54/before/c1.stdout` | blob 363 | yes, the `C1_R54:` summary | 5 |
| C1 | `.ufo/evidence/round-54/after/c1.stdout` | blob 429 | yes, the deciding `C1_R54:` summary | 5 |
| C1 | `.ufo/evidence/round-54/after/c1.stdout` | blob 429 | yes: both credited fields are 64, with `cand=<hash>` between them | 1 |
| C1 | `.ufo/evidence/round-54/after/frozen.stdout` | blob 112 | yes, `FROZEN_UNCHANGED=1` | 1 |
| C1 | (none) | — | n/a. The `59c38109` line `credited=41 lost=23` is the spotcheck's re-run, not a named receipt. `git grep credited=41 <rev> -- .ufo/evidence/round-54` returns nothing | — |
| C2 | `.ufo/evidence/round-54/after/c2.stdout` | blob 1305 | yes, deciding `C2_R54:` summary `total=0` | 8 |
| no-harm | `.ufo/evidence/round-54/after/no-harm.stdout` | blob 1020 | yes. 14 lines, each ends ` ok`, zero `RED` | 1–14 |
| no-harm | same | | yes `NOHARM coldread-floor score=8 credited=64 ok` | 2 |
| no-harm | same | | yes `NOHARM r45-freshness population=74 fresh=71 score=9 ok` | 3 |
| no-harm | same | | yes `NOHARM sources-not-shrunk base=136 rev=139 ok` | 14 |
| erratum | `.ufo/evidence/round-54/after/deciding-run.exit` | blob 20 | yes `DECIDING_RUN_EXIT=0` | 1 |
| erratum | `.ufo/evidence/round-54/after/coldread-precheck.stdout` | blob 100 | **no** for `64/64` | 1 |
| census | `.ufo/evidence/round-54/after/census.exit` | blob 2 | yes `0` | 1 |
| census | `.ufo/evidence/round-54/after/census.stdout` | blob 1604 | **no** for first-pass `W04 warnings only` | 9 is a `W01` line |
| census | same | blob 1604 | no `136` or `139` in this file | — |
| S278 | `.ufo/evidence/round-54/assimilation/S278-tempfile.py` | blob 32236 | yes | 163–165 |
| S277 | `.ufo/evidence/round-54/assimilation/S277-posix-env.html` | blob 52350 | **no** (verbatim / byte 26548) | — |
| S279 | `.ufo/evidence/round-54/assimilation/S279-tempfile-docs.html` | blob 75190 | **no** (verbatim / byte 14158) | — |

`before/c1.stdout:5`

```
C1_R54: rev=d33053f7552d c0=none credited=57 lost=7 rekeyed=0/7 readers=0/7 monitor=6/57 unstable=0 total=4 C1_R54_PASS=false
```

`after/c1.stdout:5`

```
C1_R54: rev=c21081008adb c0=99c3bc88d704 credited=64 lost=0 rekeyed=7/7 readers=7/7 monitor=8/64 unstable=0 total=0 C1_R54_PASS=true
```

`after/c1.stdout:1`

```
EXPLAIN arm1-precheck exit=0 COLDREAD_PRECHECK floor=ef19d8e1e7ba floor_credited=64 cand=c21081008adb cand_credited=64 lost=0 ok
```

`coldread-precheck.stdout:1`

```
COLDREAD_PRECHECK floor=d33053f7552d floor_credited=57 cand=c21081008adb cand_credited=64 lost=0 ok
```

`after/c2.stdout:8`

```
C2_R54: rev=c21081008adb tools=7 unusable_exit2=7 naming=7 empty_ok=7 usable_ok=7 tmp_mkdirs=0 docs=7 note=1 sources=3 total=0 C2_R54_PASS=true
```

S278:165 `        if dirname: dirlist.append(dirname)`. Lines 163–164 are `for envname in 'TMPDIR', 'TEMP', 'TMP':` and `dirname = _os.getenv(envname)`. The erratum's three-line quote matches with indent stripped.

## Findings about the spotcheck

No cited receipt is missing at `0a2010ac`. The findings below are quotes that are not in the object the spotcheck names.

1. **S277 byte and verbatim quote.** First pass: quote located at byte 26548, "24 words". Erratum: a 21-word quote, `TMPDIR This variable shall represent a pathname of a directory made available for programs that need a place to create temporary files`. That sentence is 22 words with `TMPDIR`, 21 without. Byte 26548 is an `NLSPATH` example, not this sentence (`s277-byte-26548.txt`). The definition is not a contiguous raw substring: `<dt><i>TMPDIR</i></dt>` and a newline between `temporary` and `files` (`s277-definition.txt`, raw phrase byte 42154). Whitespace-collapsed, tags deleted, the 22-word string sits at offset 26585 (37 bytes after the claim). Tags replaced by spaces, then collapsed: offset 26782. Neither is 26548.

2. **S279 byte and verbatim quote.** First pass: quote at byte 14158, "The directory named by the TMPDIR environment variable". Erratum: "The list is: The directory named by the TMPDIR environment variable". Byte 14158 is an unrelated `encoding=` signature (`s279-byte-14158.txt`). Raw `The list is` is at byte 51233, and `TMPDIR` is inside `<span>` / `<code>` so the sentence is not contiguous (`s279-list.txt`). After tag-strip and whitespace collapse the sentence is present and TMPDIR is the first list item: offset 13993 (tags deleted) or 14204 (tags replaced by spaces). Neither is 14158.

3. **Erratum attributes `coldread-precheck 64/64` to the coldread-precheck receipt.** `.ufo/evidence/round-54/after/coldread-precheck.stdout:1` says `floor_credited=57 cand_credited=64`. The 64-and-64 pair is `after/c1.stdout:1`, and that line's floor hash is `ef19d8e1`, not `d33053f7`. Same shape as R54.10: a real pair of numbers, named against the wrong file.

4. **First pass says the census receipt is `W04 warnings only`.** `census.stdout` line 9 is `tameshi	W01	S101 tierC mined used-by=corpus/knowledge/witness-equivalence-rule.md`. Counts: W01 ×1, W04 ×15, plus the `ok` line (17 lines). The erratum's later `W01/W04 only` matches. The first pass does not.

5. **R54.8 line number.** The spotcheck says the seat file `:324` asserts `on the operator's direct instruction in-session, which is the higher authority`. Line 324 is the scope-note opener. The assertion is wrapped across lines 325–326, so the exact string is not a substring until those lines are joined. The assertion is in the file. The cited line is not.

## Not findings

- `136 → 139` is not in `census.stdout` (zero hits). It is `no-harm.stdout:14`. The first pass attributes that count to a `| S### |` count, not to a line of `census.stdout`. The digits and the census receipt are different objects.
- `frozen.stdout` does not contain the words `5 amendments`. The count is `len(freeze.json["amendments"]) == 5`. The backtick quote `freeze=077d431e` is on line 1.
- The `59c38109` / `credited=41` block is not backed by a committed round-54 receipt. The spotcheck presents it as a re-run.
- Staged-package `81` and `config.yml:418` match this host now. They are not objects at the rev.
- R54.1–R54.7 and R54.9–R54.10 quotes that name a committed receipt are in that receipt, at the lines above.
- Ledger bound-entry check: none of the 23 `inputs` dumps contain `LOG.md`, `SCORECARD.md`, or `round-21/coldread/ledger.json`. That is the spotcheck's claim, and it holds for this definition of "bound" (`traces` contains `rekey-r54-99c3bc88d704`).

## Confidence

High on existence, type, size, and line match: those are `git cat-file` / `git show` at `0a2010ac`. High on the five spotcheck findings: each is a byte or line the named object does not contain, with the actual bytes saved under the receipts dir. The genuine-reader path for `61736dce` is inferred (the spotcheck says "the genuine reader's"); `T54W2Read01.json:1` is the committed reader that carries that digest. Section bytes at c0 were not re-hashed.
