# T92SC1 — draft append block for `corpus/knowledge/mutation-case-fleet-sources-census.md`

Seat: T92SC1 (lane `tameshi`, round 92). Read-only on the lane; this file and
the three probe files beside it are the deliverables. The block below is what
the L1 appends to the case note. The L1 integrates it — nothing was written
into `corpus/`.

**Integration notes for the L1 (not part of the appended block)**

1. The block is appended at the end of the note, after the round-91
   `## Admission status (appended round 91)` section. It is self-contained
   and claims no admission.
2. **Merge the S320 clause into the note's existing front-matter `source:`
   line — do not add a second `source:` line.** The note has exactly one
   `source:`-prefixed line (line 1), and two counters read it with the
   conjunct `len(src) == 1`: `.ufo/evidence/round-90/c1/measure.py:232-233`
   and `.ufo/evidence/round-91/c1/measure-v91.py:268-269`. A second
   `source:` line makes `cited` empty and drops their `source` conjunct —
   measured: a block carrying its own `source:` line turns the round-90
   counter from `C1_R90_PASS=true` into `C1_R90_PASS=false`
   (`source=false`), while the same block with the `source:` line dropped
   leaves it `true`. Evidence: `T92SC1-source-line-probe.out`, arms A/B/C.
   The round-92 counter does **not** read the note's `source:` line at all
   (it reads the `SOURCES.md` row for S320 and the round-92 lesson), so this
   constraint is about the note's own documented reproduce path, not about
   the round-92 certificate.

   The merge itself was measured, not assumed:
   `T92SC1-frontmatter-merge-probe.out` builds the recommended integration on
   scratch clones and reads each with **both** counters — arm D (merge only)
   and arm E (merge plus the `SOURCES.md` used-by update of item 3 below) —
   and both arms print `C1_R90_PASS=true` and `C1_R92_PASS=true` with
   `source=true` and `badrows=0 headers=1`. The merge is safe because the
   round-90 counter's `source` conjunct is satisfied by any cited sid above
   315 whose `SOURCES.md` row names the note in `used-by`, and S316/S317
   already do.

   The clause to merge, in the note's own `source:` style (same grammar as
   the S316/S317 clauses already there — id, title, `(docs, tier A, mined,
   opened YYYY-MM-DD)`, URL, quoted path:line, and what it grounds):

   > S320 sha256sum(1) — Arch manual pages (GNU coreutils 9.12) (docs, tier A, mined, opened 2026-11-08) — https://man.archlinux.org/man/sha256sum.1.en, `.ufo/evidence/round-92/sources/s320.txt:19`: "Print or check SHA256 (256-bit) checksums." and `s320.txt:53`: "The sums are computed as described in FIPS-180-2." (grounds the counter's `SELF_SHA256` self-pin: the pin is a digest of the instrument's own bytes, and `--check`/`--strict` are the semantics a reader uses to re-verify it)

3. **`SOURCES.md` side effect, if the note is to cite S320.** The census
   gate's `E11` rule checks that every `used-by` path exists on disk, and
   the registry convention is that a source row names the files that use it.
   S320's row currently reads `used-by: corpus/lessons/round-92.md`. If the
   note cites S320, that cell should gain
   `corpus/knowledge/mutation-case-fleet-sources-census.md` **while keeping
   `corpus/lessons/round-92.md`**: the round-92 counter's `source` conjunct
   is `LESSON_PATH in c[11]` (`measure-v92.py:319-320`), so the lesson path
   must remain in that cell or `source=false` and the round-92 certificate
   fails. Both paths exist on disk, so `E11` stays green either way.
4. Counter-safety of the block was measured, not asserted. Four probes, all
   in this directory:
   - `T92SC1-append-probe.sh` / `.out` — the real sealed round-92 counter
     over the real note plus the block, on a scratch clone: `C1_R92_PASS=true`,
     exit 0, `badrows=0 headers=1`; the same counter over the un-appended
     note at the same rev: `C1_R92_PASS=true`, exit 0.
   - `T92SC1-parse-limits-probe.py` / `.out` — the frozen counter's own
     `parse_note` over the four limit classes and the two refusal classes.
   - `T92SC1-source-line-probe.sh` / `.out` — the round-90 counter over
     three arms of the note (baseline / a block carrying its own `source:`
     line / this draft).
   - `T92SC1-frontmatter-merge-probe.sh` / `.out` — both counters over the
     recommended integration, arms D and E.

=== BEGIN APPEND BLOCK ===

## Certification status (appended round 92)

Appended; the entry above is unchanged. This block records what the round-92
sealed successor certifies about this note's twelve cells, and the limits
under which it certifies them. It asserts no admission — admission is the
closure's, and the round-92 claim R92-C1 is open until the closure lands.

### The counter

The sealed successor counter is `.ufo/evidence/round-92/c1/measure-v92.py`,
sha256 `be5a9221b36983d6c45e983c398ee9c9c088b374d36fb17e2ae67f50ad749ea9` —
the same bytes at the instrument revision `84904d41a31fb5ddde49e8bf1ad6fc2b489671a0`
and at the freeze `25f976625501663f2ea3336cc3e40499580ea59c`. (The dispatch
text for this seat carried `a6adf4a6…`, which is the earlier instrument-A
blob at `884a4dc1`; the plan's and `claims.json`'s value is the one above.)

The counter pins its own bytes, so the pin is re-derivable without trusting
the file that carries it. The digest semantics are those of S320 sha256sum(1)
— Arch manual pages (GNU coreutils 9.12) (docs, tier A, mined, opened
2026-11-08) — https://man.archlinux.org/man/sha256sum.1.en,
`.ufo/evidence/round-92/sources/s320.txt:19`: "Print or check SHA256 (256-bit)
checksums." and `s320.txt:53`: "The sums are computed as described in
FIPS-180-2." (grounds the counter's `SELF_SHA256` self-pin: the pin is a
digest of the instrument's own bytes, and `--check`/`--strict` are the
semantics a reader uses to re-verify it):

```sh
python3 -c 'import hashlib,re,sys; b=open(sys.argv[1],"rb").read(); b=re.sub(rb"^SELF_SHA256 = \"[0-9a-f]{64}\"\n", b"", b, flags=re.M); print(hashlib.sha256(b).hexdigest())' .ufo/evidence/round-92/c1/measure-v92.py
```

which prints `723562ed5b20e1a914d9addbce9007b8edf1c962c8237592dbac3b39e5509c2c`
— the digest with the single `SELF_SHA256 = "<64 hex>"` line removed; the raw
file digest is the sha256 above. A post-freeze edit of the instrument is inert:
it refuses at setup with `C1_SETUP self-pin-mismatch`, exit 2, which is what
the committed `selfpin-edit` receipt shows. The counter also refuses any
verdict-bearing row whose id is outside the spec's set C01–C12, so a second
table under ids the lane does not key is refused rather than hidden behind.

### What the counter measured

Under that counter the twelve verdicts above are reproduced and every conjunct
holds:

- `C1_SUMMARY … n=12 killed=5 survived=7 inconclusive=0 unstable=0 invalid=0 trivial=0 witnessed=7/7 note=present mismatched=0 badrows=0 headers=1`
- `C1_CONJUNCTS selfpin=true pin=true spec=true green=true canary=true invalid0=true trivial0=true inconclusive0=true unstable0=true note=true ids=true mismatched0=true figure=true witnessed=true source=true coverage=true n_min=true`
- `C1_R92_PASS=true`, exit 0

The honest receipt is the committed positive control
`.ufo/evidence/round-92/pre-freeze/controls/pos-real.out` — the real note,
registry row and lesson at the instrument revision, one edit-free state, exit 0
(`C1_SUMMARY rev=3102be9998faabdb04385bef3ff7a2269d63dbae …`). The do-nothing
receipt is `pre-freeze/controls/nowork-base.out`: `C1_SETUP spec-absent-at-rev`,
exit 2, at the base `63172b9889475103aeca976d37389d204010dd11`.

### The control battery

`.ufo/evidence/round-92/pre-freeze/controls/` holds the 25 receipts and the
summary `C1-summary.txt`, which the driver derives from the receipts on disk:
25 states, 25 `MATCH`, no `MISMATCH` (the driver's own stdout line is
`C1_CONTROLS states=25 matched=25 mismatches=0`). Among them:

- the refusal states this round was frozen to add — `out-of-set` and
  `out-of-set-letters` (a second verdict table under ids the lane does not
  key), `unkeyed-row`, `dup-row`, `position`: each `ids=false`, exit 1;
- the seal states `replace-honest` and `replace-false-sealed`:
  `C1_SETUP replace-refs-present`, exit 2;
- the self-pin state `selfpin-edit`: `C1_SETUP self-pin-mismatch`, exit 2;
- the three counter-removal mutants `D01`, `D01D02` and `D03`, each of which
  turns a state the frozen counter refuses into `C1_R92_PASS=true` — the
  removals are what the protections are worth.

### Limits

The counter certifies that the twelve cells are true, not how they were
obtained. Its parser keys only what this note presents as its verdict table,
and these classes are outside it — declared limits, not kills:

- Fenced code blocks and HTML tables are not keyed: they are not Markdown
  tables the note presents as its verdict table. A verdict row inside a fence,
  or an HTML table, is invisible to the parser.
- Verdict words in prose are ignored. The prose, the survivor table and the
  arms are not counted.
- A note that copies the committed predictions instead of the measured receipt
  carries the same cells and passes: the counter certifies that the cells are
  true, not how they were obtained (round 90's critic probe,
  `.ufo/waves/round-90/w1/T90C1.md` probe A; recorded as disputed and not
  counted as a kill in `corpus/lessons/round-90.md`). This note's cells are
  copied from the measured receipt, and the receipt path is named above.
- A table row with an escaped `\|` inside a cell shifts the columns and
  refuses — strict, and not exercised by this note.
- The canary shows the copy runs, not which selftest arm executed a mutated
  line.

One reading has changed since round 90 and is corrected here. The round-90
note recorded that the counter read this note's `source:` line; the round-92
counter does not. Its `source` conjunct is read from the `SOURCES.md` row for
S320 and from `corpus/lessons/round-92.md`, while the note itself contributes
only its verdict table and the `measured:` line. The front-matter `source:`
line of this note records the citation for readers.

=== END APPEND BLOCK ===
