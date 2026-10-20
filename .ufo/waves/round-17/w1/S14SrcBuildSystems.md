# S14 — Build Systems à la Carte: the verifying-traces definition

Seat: S14SrcBuildSystems (scout) · round 17 / wave 1 · 2026-10-20.
Question assigned: find an official open copy, locate the verifying-traces
definition, record an access date, a ≤25-word verbatim quote with its location,
and draft a SOURCES.md row in the lane contract shape; note what it teaches for
C1 (input-keyed cold-read credit).

**Answer in brief.** The published open copy is the PACMPL ICFP 2018 article,
served by Microsoft Research, DOI 10.1145/3236774, 29 pp., sha256
`d6c175a4…ede`. The definition is §4.2.2 "Verifying Traces", printed p. 79:14.
The definition sits in the paper's four-way taxonomy of rebuilders (§4.2.1–4.2.4):
recording the hashes of the dependencies **used last time**, and rebuilding when
one differs, is the whole of `verifyVT`. The 2020 JFP manuscript restates the same mechanism, and adds
the explicit per-hash sentence, but the copy on MSR is a pre-acceptance
manuscript, so the row anchors the published PACMPL text.

## 1. Which copy was opened, and how it was established

| Step | Command | Observed |
|---|---|---|
| Landing page | `curl -sL -o msr-landing.html -w 'landing %{http_code}\n' https://www.microsoft.com/en-us/research/publication/build-systems-la-carte/` | `landing 200`; 170614 B; `<title>Build systems a la carte - Microsoft Research</title>`; page links `.../wp-content/uploads/2018/03/build-systems-final.pdf` |
| Published PDF | `curl -sL -o bsf.pdf -w 'pdf %{http_code} %{size_download}\n' https://www.microsoft.com/en-us/research/wp-content/uploads/2018/03/build-systems-final.pdf` | `pdf 200 728559` |
| Blob pin | `sha256sum bsf.pdf` | `d6c175a48cc908ca3f185e1fb4620e3278c5655218ac687d83dfa7f405624ede` |
| Metadata | `pdfinfo bsf.pdf` | `Title: Build Systems à la Carte`, `Author: Andrey Mokhov, Neil Mitchell, and Simon Peyton Jones`, `Pages: 29`, `CreationDate: Fri Jul 13 20:01:50 2018` |
| Venue, from p.1 | `pdftotext -f 1 -l 1 bsf.pdf -` | `Proc. ACM Program. Lang. 2, ICFP, Article 79 (September 2018), 29 pages. https://doi.org/10.1145/3236774` |
| DOI resolves | `curl -sI -o /dev/null -w '%{http_code} %{redirect_url}' https://doi.org/10.1145/3236774` | `302 https://dl.acm.org/doi/10.1145/3236774` (registration confirmed; direct ACM fetch returns 403 to a plain client and was not the opened copy) |
| Second URL spelling | `curl -sL -o bsf-alt.pdf -w 'alt %{http_code} %{size_download}\n' https://www.microsoft.com/en-us/research/uploads/prod/2018/03/build-systems.pdf`, then `sha256sum bsf.pdf bsf-alt.pdf` | `alt 200 728559`; both files `d6c175a4…ede` — one blob at two MSR paths |

Access date recorded: **2026-10-20**. No installs this seat (curl and
`pdftotext` already present). Scratch root for every command in this report:
`W=/tmp/tameshi-r17w1-S14SrcBuildSystems-v8KCxT`, created with
`mktemp -d /tmp/tameshi-r17w1-S14SrcBuildSystems-XXXXXX`; the fetches and the
census fixture live under `$W`, and each command below was run with `cd "$W"`.

The JFP 2020 version was also opened, for corroboration only:

| Step | Observed |
|---|---|
| `curl -sL -o msr-jfp-page.html -w 'jfp-landing %{http_code}\n' https://www.microsoft.com/en-us/research/publication/build-systems-a-la-carte/` | `jfp-landing 200`; title `Build systems a la carte: theory and practice`; links `.../wp-content/uploads/2020/04/build-systems-jfp.pdf` |
| `curl -sL -o jfp.pdf -w 'jfp-pdf %{http_code} %{size_download}\n' https://www.microsoft.com/en-us/research/wp-content/uploads/2020/04/build-systems-jfp.pdf` | `jfp-pdf 200 769395`; sha256 `4e59a833…56eb`; 54 pp.; `CreationDate: Tue Feb 4 06:07:51 2020`; p.1 reads `Under consideration for publication in J. Functional Programming` |
| DOI `10.1017/S0956796820000088` | `302 https://www.cambridge.org/core/product/identifier/S0956796820000088/type/journal_article` (registered) |

So the JFP DOI is real, but the open file is the 2020-02-04 manuscript, not the
accepted article. Anchoring the row on it would claim a text nobody has opened
in its published form.

## 2. Where the definition is, and what the section actually says

`pdftotext -f 14 -l 14 bsf.pdf - | sed -n '42,43p'` returns the section's
second sentence verbatim (line-number shown as extracted):

```
4.2.2 Verifying Traces. An alternative way to determine if a key is dirty is to record the values/hashes of dependencies used last time, and if something has changed, the key is dirty and must
be rebuilt ś in essence a trace which we can use to verify existing values. For traces, there are two
```

(`ś` is `pdftotext`'s rendering of the en dash in this PDF's font encoding; the
quote below stops before it, so the quote itself is unaffected.)

What §4.2 establishes, in its own terms:

- §4.2 "The Rebuilder: Determining Out-of-date Keys" names four fundamental
  ways to decide dirtiness: a dirty bit (§4.2.1), verifying traces (§4.2.2),
  constructive traces (§4.2.3), deep constructive traces (§4.2.4).
- The verifying trace is `VT k v`, built by two operations, quoted from the page:
  `recordVT :: k -> Hash v -> [(k, Hash v)] -> VT k v -> VT k v` and
  `verifyVT :: (Monad m, Eq k, Eq v) => k -> Hash v -> (k -> m (Hash v)) -> VT k v -> m Bool`.
  `recordVT` is called after a successful build with the key, the hash of its
  value, and **the list of hashes and dependencies**; `verifyVT` is called with
  the key and a function that fetches the current hash of any key.
- "Rather than storing (large) values v, the verifying trace VT stores only
  hashes, of type Hash v … it constitutes the build system's memory."
- "True indicates that the current value is already up to date, and False
  indicates that it should be rebuilt."
- "A verifying trace … support[s] dynamic dependencies and minimality;
  furthermore, all traces except for deep traces support early cutoff."
- Table 2, p. 79:16, places verifying traces at Ninja (topological scheduler)
  and Shake (suspending); Fig. 9, p. 79:20, is the executable model:
  `upToDate <- verifyVT key (hash value) (fmap hash . fetch)`, then on
  non-up-to-date `recordVT` with the new dependency hashes.

JFP manuscript corroboration, §5.2 "Verifying Traces", printed p. 23, is more
explicit about the per-dependency comparison:

> If any of the hashes is different, we rebuild util.o, and record a trace with the new values.

(18 words; page 23 lines 28–29 of the page text, sentence rejoined across the
line break.)

## 3. The quote for the Gate (≤25 words)

> record the values/hashes of dependencies used last time, and if something has changed, the key is dirty and must be rebuilt

- Location: §4.2.2 Verifying Traces, printed p. 79:14 (PDF page 14 of 29), in
  the sentence beginning "An alternative way to determine if a key is dirty …".
- Length: **21 words** (counted with `re.findall(r"[A-Za-z0-9][A-Za-z0-9/_.-]*", q)`).
- Verbatim notes: the PDF breaks the sentence at `val-` / `ues/hashes` and at
  `must` / `be rebuilt`; the quote is the dehyphenated, rejoined span. Case,
  punctuation and the `values/hashes` slash are as printed. The quote starts
  mid-sentence by design, to stay under 25 words.
- Membership receipt: `pdftotext -f 14 -l 14 "$W/bsf.pdf" -`, whitespace
  flattened, contains the quote verbatim → `True`. A first pass that compared
  the blockquote line *with* its trailing newline returned `False`; the diff
  showed the sole difference was `' '` → `'\n'`, i.e. the harness, not the
  text.

## 4. SOURCES.md row draft

Placeholder id per the seat brief (L1 assigns); `## Id allocation` in
`corpus/SOURCES.md` says "Next unused id: S058", and the nearest existing rows
S052–S057 are round-16. If L1 allocates **S058**, this row is paste-ready as
written.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S0xx | Build Systems à la Carte (Mokhov, Mitchell, Peyton Jones; PACMPL 2, ICFP, Article 79, September 2018; DOI 10.1145/3236774) — https://www.microsoft.com/en-us/research/wp-content/uploads/2018/03/build-systems-final.pdf | paper | A | the verifying-traces rebuilder — how a previously built value is checked against later inputs | §4.2.2 Verifying Traces p. 79:14 @ PACMPL 2, ICFP, Article 79, published PDF sha256 d6c175a48cc908ca3f185e1fb4620e3278c5655218ac687d83dfa7f405624ede | rebuild when a recorded dependency hash differs: the trace of hashes is what lets a later build verify an existing value instead of trusting a clean bit | queued | 2026-10-20 | 730d | — |

Shape checks actually run:

- Field count: 12 `|` delimiters, 11 cells, gawk NF=13 — same as the contract
  header row; no `|` inside a cell.
- Lane validator, positive: the row was **extracted from this report** and
  `S0xx` substituted by `S058`, then placed in a fake fleet root
  (`$W/fake-root`, one-lane `shokunin.conf`, lane `fake-shokunin`) holding
  only the header plus that row —
  `scripts/sources-census.sh validate --root "$W/fake-root" --today 2026-10-20 fake`
  → `fake	ok	$W/fake-root/fake-shokunin/corpus/SOURCES.md`, **exit 0**.
- Placeholder behaviour: the same extracted row with `S0xx` unsubstituted
  yields `fake	E02	S0xx`, **exit 1** — the id grammar is enforced, so L1 must
  allocate the number before appending.
- Negative control: the row with its `tier` cell deleted yields
  `fake	E01	S058 fields=10`, **exit 1**. The check can fail.
- `status queued`, `used-by —`: nothing cites the row yet; a `mined` row with
  `—` would only warn (W03), but `queued` is the honest status.
- Tier A scope is the section's own claim, not "build systems" generally.

Paste-ready `## Gate` line (SOURCES contract rule 1) once the id is allocated:

```
S0xx Build Systems à la Carte — https://www.microsoft.com/en-us/research/wp-content/uploads/2018/03/build-systems-final.pdf (DOI 10.1145/3236774), opened 2026-10-20; §4.2.2 Verifying Traces p. 79:14: "record the values/hashes of dependencies used last time, and if something has changed, the key is dirty and must be rebuilt" (21 words) — grounds input-keyed credit: verify the recorded input hashes, not a stored clean bit.
```

## 5. What it teaches for C1 (input-keyed cold-read credit)

C1 says: a cold-read entry that executed commands credits its SKILL.md bucket
only if every lane input it ran against still has its recorded sha256 at the
measured rev. The source supplies the general form of that rule.

- **The mechanism is `verifyVT`.** Credit is not "this key was built once"; it
  is: look up the trace recorded at build time, fetch the current hash of each
  dependency named there, and skip only if none differs. Difference → rebuild
  and record a new trace. Mapped onto the ledger:
  entry = key; the executed commands = the build step; `inputs{path: sha256}`
  = the `[(k, Hash v)]` list; `measure.py` re-reading each path's blob at REV
  = the `fetchHash` callback; "credits iff every input hash matches" = `verifyVT`
  returning `True`. The mapping is [INFERENCE]; the mechanism is quoted.
- **The round-16 harm is the dirty-bit alternative, by name.** R16-C2b found a
  bucket credited by its section sha alone, while `tools/mutate-and-run.sh`,
  which its commands run against, had moved (`round-16-verifier-spotcheck.md`
  §2, §6 defect 3). In the paper's vocabulary the ledger held a dirty bit per
  bucket — "verified" — with no dependency trace. A dirty bit cannot answer
  *clean against what?*: §4.2.1 shows Excel must over-approximate by marking
  transitive dependents dirty, and Make's mtime bit is repurposed file-system
  state that backup software can invert. That is exactly the failure mode C1
  repairs: a recorded result whose inputs are unnamed stays "clean" across the
  very change that invalidated it.
- **Why input-keyed, not tree-keyed.** §4.2.2 records the dependencies *used
  last time*, not the whole store. Hashing the whole tree at REV would be the
  §4.2.1 over-approximation — any unrelated commit would uncredit every bucket.
  Input-keyed hashes keep credit where the executed surface is byte-identical
  and drop it exactly where it moved. The source therefore justifies C1's
  existing design rather than proposing new machinery.
- **Early cutoff, the useful half.** The same page states traces support early
  cutoff. Read against C1: a bucket may keep credit across a rev change when its
  recorded input hashes are unchanged, so wave-2 re-reads are spent only where
  hashes drift — not on every bucket, and not on none.
- **Boundary of what the source proves.** The paper is about build *values*,
  not audit records. It supports "a result is checkable only against the hashes
  of the dependencies it used", not "a cold-read report is valid". Two limits
  the lane must keep: (i) the trace must be recorded at execution time — a
  report that fills `inputs` after the fact is only as good as its capture, and
  `verifyVT` cannot see a dependency the tracer missed (that hole belongs to
  `trace-inputs.py`'s strace coverage, not to this row); (ii) §4.2.2's guarantee
  is about the recorded set, so a command that reads an *unrecorded* input is
  outside it. [INFERENCE for both limits; they are consequences, not quotes.]

## 6. Search-log note (SOURCES contract rule 5), ready to append

- 2026-10-20 — **C1 build-reuse grounding** (S14 seat). Question: what does an
  authoritative source say makes a previously produced result re-checkable
  against later inputs? Where: the MSR publication pages for
  `build-systems-la-carte` and `build-systems-a-la-carte`, both fetched with
  `curl -sL` on 2026-10-20; bodies pinned by sha256. Identified 2 copies of one
  article family · screened 2 · included 1 (published PACMPL ICFP 2018 PDF) ·
  excluded 1 (JFP 2020 file is a 2020-02-04 pre-acceptance manuscript, kept as
  corroboration). `dl.acm.org/doi/10.1145/3236774` returned HTTP 403 to a plain
  client; the DOI resolver's 302 established registration, and MSR supplied the
  opened bytes. Stop rationale: the definition was located in the published
  text with a page-level anchor and a 21-word quote; the only remaining open is
  the Cambridge JFP rendering, which is not needed for the definition.

## 7. Remaining unknowns / cautions for integration

- The published JFP (Cambridge) text was not opened; only the Feb 2020
  manuscript. A JFP-paginated quote would be a second open, and a second row
  only if the lane wants that version citable separately.
- `dl.acm.org` is unreadable to this client (403); the open-access status of
  PACMPL is [INFERENCE] from the MSR final PDF and the DOI registration, not
  from the ACM page.
- One row, not two: the two versions state the same mechanism; a second row on
  the same ground would be duplicate-method material.
- No edits were made to lane files; this report and `/tmp` scratch only.

## Verdict

**built** — official open copy opened 2026-10-20, definition located at §4.2.2 p. 79:14 with a 21-word verbatim quote, and a census-clean SOURCES row drafted whose teaching is the input-keyed `verifyVT` rule C1 adopts.
