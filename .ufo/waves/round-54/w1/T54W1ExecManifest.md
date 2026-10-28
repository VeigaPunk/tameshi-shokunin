# T54W1ExecManifest — section manifest for the 23 lost headings at C0

Seat: T54W1ExecManifest (executor, wave round-54-w1). Judged axis: calibration.
Item: compute start, end and `section_sha256` at C0 for each of the 23 headings in
`.ufo/evidence/round-54/c1/lost-headings-at-c0.json` with
`.ufo/waves/round-54/reader-section.py`, write them as
`.ufo/waves/round-54/w1/section-manifest.json`, and record the SKILL.md blob hash at C0
in the same file under `skill_sha256`. That file is the manifest the binder and the C1
counter are compared against.

Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`. C0:
`59c38109bf119d0e9d4f878644a82babc937bc1e`.

## Axes I moved

- **calibration (primary)** — every span is the oracle's own answer at C0, re-derived
  independently from the blob, and reconciled against the counter's own section map.
- **evidence completeness** — every number below is a command plus its output, saved
  under `w1/T54W1ExecManifest-receipts/`.
- **no side effects** — nothing outside `w1/` written in the lane; scratch removed.

## Deliverable

`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-54/w1/section-manifest.json`

Shape: one JSON object, because a top-level list cannot carry the required
`skill_sha256` key:

```json
{"cand": "59c38109bf119d0e9d4f878644a82babc937bc1e",
 "skill_sha256": "e0e0b4d0134f4555951183dec11872ff6665f7c1f94d3958fa2888df3ef47ff9",
 "sections": [{"heading": "...", "cand": "...", "start": 17, "end": 40,
               "section_sha256": "..."}]}
```

Each entry is the reader-section.py output object verbatim (`heading`, `cand`, `start`,
`end`, `section_sha256`), in the order of `lost-headings-at-c0.json`.

|#|heading|start|end|section_sha256|
|-|-|-|-|-|
|1|## Standing rules|17|40|164390276b453ddb23bcb3633269217afc8ee9d47a9e470af6fece181a5743f7|
|2|## Mutation-sweep recipe — numbered steps; bounded cold-read evidence|142|256|c413b4268eb842637f17df2396d06ab53cbffe5ba4fb063b6ee37165a800e65e|
|3|### The boundaries — what a service run is not|869|893|9aa3c41cfd365e32cc8e1feb1155e0be96df016dd5ea5c6d3ffa80aa8df3ba63|
|4|## The leg ledger — replay, receipt, and how it is read (round 7, measured)|932|945|430dd86f25b6ce3d5ed51012d54de7cdad7213c6353eb7701323de762b9fb993|
|5|### Using the ledger|946|977|808dad50760d693bc9e952a32a08cff129a74fd56163876aa3b656f9a9775d04|
|6|### The tick and the pin read|1034|1082|ca86e98de294306fca4f2cbc060555b05eb036967ad333d907b761e09fb70805|
|7|### Triggers T1–T3 and the re-pin rule|1083|1105|2350210704efcc3becfbcd40a63775ad591910039744ac6d072881b3deef7801|
|8|### The service's limits — what tameshi refuses to mutation-test|1265|1294|37d63abf882e89d8103fb2618d8622c78da60aecfac75352851687e42eea7590|
|9|## The operator's runbook and the six-leg regression (round 10, measured)|1295|1303|636e850f885cb39904d100f67446e1039aa48c6510c2a66ea6e6d5aaa089faf7|
|10|### The operator's runbook — `corpus/knowledge/operator-runbook.md`|1304|1324|c246d3743e0a441224ece3e2dcc195a359f365e23a9e757fe0441a5ea71055ed|
|11|## Repeated controls and gate registry — round 12|1504|1523|2613c4fe5c89d2971d16622a0cf1888acc40b8c26a137b9c4bd120cc95053a96|
|12|### Gate/probe registry|1524|1541|99285e24a71a8d2a0ea3fd6bcafe7e080acb23bfd653e7cbb3b71dfdc5144c77|
|13|## Pin disposition and provenance correction — round 13|1542|1572|ad8d6c4010f2c584a8fd34795625d66ab1a7ffcc91463a49e6d122ca06e4bf15|
|14|### Round-13 gate/probe registry|1573|1588|896722c4941841f228810678befe82e9910cc66eb67c3de45d7561ce4668566d|
|15|## Effective expectation reconciliation — round 14|1589|1622|9640e5dc426f1f9ed7050e2443ac96c478e008ed9c2948ad59790da8aa977e3d|
|16|### Round-14 historical registry — superseded by round 15|1623|1634|06a6864fb05fd63df168597696407397c7d3f4d47337556c25ab60393fb959af|
|17|## Context gate classification and explicit exit classes — round 15|1635|1701|132cfb9ef1aa07111af42389e4fe862152e3118b3a8bb66f1d84a6a332e7edf6|
|18|### Round-15 gate/probe registry|1702|1732|da6ef23c23f06af0c420a87476364031b107f82cf16260900040a6cb3fdac516|
|19|## Live-tree re-pin and entry-command monitor — round 17|1840|1871|037c9df3076fc7ada495b906b9bf458e9d06099bfaf9d1270b88de0acb4151f3|
|20|### Round-17 gate/probe registry — re-pin and monitor|1872|1880|8a92f71e046aae243294c42153c6ed183ccd41edf4647ff9520e35a26b9c9643|
|21|### Round-18 gate/probe registry — routed-defect closure|1951|1963|1f0a60ec99834f64de35d40b845f2c71381b15e8b24310eaf8ffa8028379e439|
|22|### Round-21 gate/probe registry — finite environment differential|1990|2129|eccd3ec82207fa69cee544f8f4ebfc0f9a473fe7254b8041ae2f5924f8d00a06|
|23|### Round-26 gate/probe registry — report interop|2158|2197|cc23587b353fb780d4310aebc7277e4030729ae767850e2e826d2ff151bdea52|

`skill_sha256 = e0e0b4d0134f4555951183dec11872ff6665f7c1f94d3958fa2888df3ef47ff9`
(198186-byte SKILL.md blob; git blob id `95ae52bbc22687c9ca9cfe5e95024636e75e78a0` — a
different digest, sha1 of the blob header+bytes, recorded only so the two hashes are not
confused).

## How it was produced

Scratch: `/fast/scratch/hyaku/tameshi-r54/T54W1ExecManifest` (`export TMPDIR=` that tree's
`tmp/`, `trap 'rm -rf -- "$S"' EXIT`; tree removed before yielding).

```
$ export TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W1ExecManifest/tmp
$ cd /fast/scratch/hyaku/tameshi-r54/T54W1ExecManifest && python3 manifest.py
skill_sha256 e0e0b4d0134f4555951183dec11872ff6665f7c1f94d3958fa2888df3ef47ff9 blob_bytes 198186
17   40    ## Standing rules                                                164390276b453d… ok
...
2158 2197  ### Round-26 gate/probe registry — report interop                cc23587b353f… ok
wrote /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-54/w1/section-manifest.json
```

(`manifest.py` calls the oracle once per heading:
`python3 <LANE>/.ufo/waves/round-54/reader-section.py <LANE> 59c38109bf11… "<heading>"`,
parses the JSON it prints, and never re-derives the numbers itself. Full table:
`T54W1ExecManifest-receipts/manifest-run.out`.)

## What I checked, and the output

1. **Oracle agreement, all 23 headings.** Every `reader-section.py` invocation exited 0 and
   printed a JSON object; 23/23 resolved (no `no such section`). Receipt:
   `manifest-run.out`.
2. **Independent re-derivation of every span and hash** — a separate parser in
   `verify.py` re-split the C0 blob (own fence-aware `^#{1,3}(\s|$)` scan, own
   trailing-blank trim, own sha256) and compared against the manifest, including
   that line `start` is the heading text, line `end+1` is a heading or EOF, spans are
   ordered and non-overlapping, and the heading set/order equals
   `lost-headings-at-c0.json`:

   ```
   $ python3 verify.py
   lines=2197 headings_at_c0=63 manifest_sections=23
   skill_sha256=e0e0b4d0134f4555951183dec11872ff6665f7c1f94d3958fa2888df3ef47ff9 (file bytes=198186)
   CHECK PASS
   ```
   Receipt: `T54W1ExecManifest-receipts/verify.out`.
3. **The counter/binder's own comparison key.** The C1 counter builds
   `sections = {s['heading']: s for s in r18_mod.sectionize(skill_raw)}` at REV
   (`.ufo/evidence/round-54/c1/measure.py:165-168`) and compares
   `section_sha256` to that. I loaded the round-18 `sectionize` from the C0 blob and
   compared all 23 triples to the manifest:

   ```
   sectionize sections at C0: 64
   manifest sections compared: 23
   mismatches: none
   skill_sha256 matches blob sha256: True
   ```
4. **The lost set itself.** Ran the frozen precheck inputs (round-21 monitor at floor
   `ef19d8e1e7ba` and at C0) and applied the precheck's set difference:

   ```
   monitor(floor ef19d8e1e7ba) sections=64 credited=64
   monitor(cand 59c38109bf11) sections=64 credited=41
   lost=23 gained=[]
   set(lost) == set(lost-headings-at-c0.json): True
   preamble section measured separately: heading='' credited_at_c0=True
   ```
   Receipt: `lost-set-compare.out`. So the 23 headings I manifest are exactly the 23 the
   precheck calls lost — no extra, none missing. (`sectionize` yields 64 sections at C0
   because the preamble is a section with heading `''`; 63 real heading lines + preamble
   = 64, which is also why `floor_credited=64` and `41 + 23 = 64` hold.)
5. **The C1 counter at C0, end to end** (`--work` an empty scratch dir):
   `C1_R54: rev=59c38109bf11 c0=none credited=41 lost=23 rekeyed=0/7 readers=0/7
   monitor=6/41 unstable=0 total=4 C1_R54_PASS=false`, rc=1. Receipt: `counter-c0.out`.
   The 41/23 split matches the frozen claim; `readers=0/7` and `rekeyed=0/7` are the
   pre-wave state (no reader reports or re-key dir exist yet at C0), not defects of this
   manifest.
6. **Blob hash, computed twice by different routes** (`git show … | sha256sum` and
   `hashlib.sha256` over the same bytes): identical,
   `e0e0b4d0…f47ff9`. Receipt: `skill-hash.out`.
7. **Census conformance** (start and end of my item):
   `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
   /home/vgpnk/Projects/shokunin tameshi` → rc=0 both times (139-row range,
   `ok /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md`; the W01/W04
   duplicate-URL and tierC advisories it prints are pre-existing and unrelated).

## Risks / notes for the binder and the counter

- **Shape decision.** The item asks for "a list of those objects" *and* for
  `skill_sha256` "in the same file under `skill_sha256`". A top-level JSON array cannot
  carry a key, so the file is an object `{cand, skill_sha256, sections:[…]}` and the list
  lives at `sections`. A consumer that iterates the root must read `.sections`; anything
  keyed by heading can index it on `heading`.
- **`cand` is repeated per entry** (verbatim from `reader-section.py` output) so an entry
  is self-describing; all entries carry the same `59c38109bf11…`.
- **Spans are line numbers in the C0 blob** (`git show C0:SKILL.md`), 1-based, inclusive;
  they are not working-tree line numbers — this round's edits after C0 will shift them,
  and the manifest is correct only against C0, which is what the counter keys on.
- No production lane file was edited; the only writes are
  `w1/section-manifest.json`, this report and
  `w1/T54W1ExecManifest-receipts/`. No tool installed or upgraded (nothing was needed);
  no git/jj mutation was run.

## Receipts

- `T54W1ExecManifest-receipts/manifest-run.out` — 23 oracle invocations, one line each.
- `T54W1ExecManifest-receipts/verify.out` — independent span/hash re-derivation, CHECK PASS.
- `T54W1ExecManifest-receipts/lost-set-compare.out` — floor/C0 monitor sets, lost set,
  precheck equality, input JSON digests.
- `T54W1ExecManifest-receipts/counter-c0.out` — C1 counter at C0 (`credited=41 lost=23`).
- `T54W1ExecManifest-receipts/skill-hash.out` — sha256 and git blob id of `C0:SKILL.md`.
