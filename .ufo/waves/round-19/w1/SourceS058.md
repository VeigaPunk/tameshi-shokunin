# SourceS058 — round-19 W1 source re-open (scout, advisory)

Seat `TameshiR19-2.SourceS058`, 2026-10-21. This report is advisory only. It
changes nothing in the registry or production, and it closes nothing.

**Verdict.** S058 re-opens cleanly. The live PDF digest equals the row's
digest, the quote is verbatim at its stated location, and the row bytes have
not changed since round 17.
**Recommendation: USE it, scoped and secondary,** only for the round-19
*bounds*: a historical replay does not establish current-input equality, and
receipts are bound by value hashes. **REJECT it** as support for the C1 count
(0/5 → 5/5), R18-2, R18-3, receipt authenticity, argv or exit correctness, and
any exact-revision rule.

## 1. Registry row (observed)

- `corpus/SOURCES.md:67`, S058. `awk '/^\| S058 \|/'` gives row sha256
  `b95853ec5337c84f899dae675ef32c0acae97384a29d113403f159c67b0260c5`. The row
  is identical at four points: `eb7838b` (round-17 landing), `7243e7f`
  (round-19 baseline), `21e7932` (round-19 landed correction) and the
  worktree. `NF=13`, so the row has 11 cells.
- Row cells:
  - kind `paper`, tier `A`
  - scope: "the verifying-traces rebuilder — how a previously built value is
    checked against later inputs"
  - anchor: `§4.2.2 Verifying Traces p. 79:14 @ published PDF sha256 d6c175a4…4ede, fetched 2026-10-20`
  - status `mined`, opened 2026-10-20, recheck `730d`. [INFERENCE] The next
    recheck falls due 2028-10-19, so it is not due now.
  - used-by `corpus/knowledge/input-keyed-coldread-credit.md`. That file
    exists and cites S058 at `:1` and `:28`.
- The re-open agrees with round-17 `.ufo/waves/round-17/w2/ReopenS058.md:150-154`
  ("Holds").

## 2. Re-open: commands and outcomes

Scratch directory: `/tmp/tameshi-r19-S058/` (disposable).

```
curl -sSL --max-time 120 -A '…' -o build-systems-final.pdf -D headers.txt \
  https://www.microsoft.com/en-us/research/wp-content/uploads/2018/03/build-systems-final.pdf
  → http=200 size=728559 type=application/pdf
    Date: Wed, 21 Oct 2026 05:49:23 GMT; last-modified: Fri, 28 Feb 2025 23:30:20 GMT; etag "67c2470c-b1def"
sha256sum build-systems-final.pdf
  → d6c175a48cc908ca3f185e1fb4620e3278c5655218ac687d83dfa7f405624ede   (= row anchor digest; no drift)
pdfinfo → "Build Systems à la Carte", 29 pages, pdfTeX-1.40.17 / acmart 2018/04/14 v1.53, created 2018-07-13
pdftotext -layout -f 1 -l 1 → "Lang. 2, ICFP, Article 79 (September 2018), 29 pages. https://doi.org/10.1145/3236774";
  CC BY 4.0 notice; "© 2018 Copyright held by the owner/author(s)."
pdftotext -layout -f 14 -l 14 → line 1 "79:14  Andrey Mokhov, Neil Mitchell, and Simon Peyton Jones";
  "4.2.2 Verifying Traces." at p14.txt:41; §4.2.2 continues onto p. 79:15
curl https://dl.acm.org/doi/pdf/10.1145/3236774 → http=403, 5,566-byte HTML (sha256 73d13474…ef9f)
```

That first shell line also ran `which … mutool`. It exited 1 because mutool is
absent; the curl, sha256sum and pdf steps all succeeded.

**Access date: 2026-10-21** (05:49:23Z).

Quote check: Python over `pdftotext -f 14 -l 14` output, in both the raw and
layout renderings. The script joins `-\n` hyphen wraps and collapses
whitespace.

```python
import re, subprocess
d='/tmp/tameshi-r19-S058/'
raw=subprocess.run(['pdftotext','-f','14','-l','14',d+'build-systems-final.pdf','-'],capture_output=True,text=True).stdout
lay=open(d+'p14.txt').read()
norm=lambda t: re.sub(r'\s+',' ',re.sub(r'-\n\s*','',t))
q="record the values/hashes of dependencies used last time, and if something has changed, the key is dirty and must be rebuilt"
for name,t in (('raw',raw),('layout',lay)):
    n=norm(t); print(name, n.find('4.2.2 Verifying Traces'), n.find(q), n.count(q))
print(len(q.split()))
```

Output: `raw 3432 3512 1`, `layout 3432 3512 1`, `21`. In both renderings
the heading comes before the quote, the quote occurs exactly once, and it is
21 words long.

## 3. Located quote (≤25 words)

> "record the values/hashes of dependencies used last time, and if something
> has changed, the key is dirty and must be rebuilt"

- Location: §4.2.2 Verifying Traces, p. 79:14. Mokhov, Mitchell, Peyton
  Jones, PACMPL 2 (ICFP), Article 79, September 2018, DOI 10.1145/3236774.
- PDF sha256 `d6c175a4…4ede`; accessed 2026-10-21.
- 21 words. The `val-`/`ues` line wrap is joined. The dash after "rebuilt"
  extracts as `ś` and falls outside the quote.

Supporting quote for a limit (p. 79:15, 16 words): "After successfully
building a key, we call recordVT to add a record to the current VT".

## 4. Tier scope and limits

Tier A holds only for the definition and rebuild rule of verifying traces
inside the paper's build-system model. The tier is scoped, never global
(`/home/vgpnk/Projects/shokunin/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md:26-30`,
"original paper").

- **L1 — domain.** The paper is a formal model of build systems written in
  Haskell. It is not a source on receipts, provenance or audit. Applying it
  to receipts is the lane's [INFERENCE], and that application does not
  inherit tier A.
- **L2 — keyed by inputs, not by revision.** A value stays current while its
  recorded dependency hashes match. The paper says `verifyVT` returns
  "True indicates that the current value is already up to date" (p. 79:15).
  - Under that rule, S058 would allow reuse of the `a85f710` 60/60 result at
    `4b7c682` if every recorded input hash matched.
  - S058 therefore cannot ground the verifier's stricter requirement of a
    receipt at the cited revision
    (`corpus/lessons/round-18-verifier-spotcheck.md:201-204`). That
    requirement rests on the lane's evidence standard and QUALITY 39.
- **L3 — trust.** In the model, the build system itself writes the trace
  after a successful build (§3 quote). The paper says nothing about forged,
  laundered or mis-invoked records, argv, or exit codes. It cannot support
  "the run happened" or R18-4's actual defect (argv missing `mode`, exit 64).
- **L4 — completeness.** The model captures dependencies through `fetch`
  (dynamic dependencies, p. 79:15). Lane receipts record only the inputs
  their author lists. Inputs left outside the key are the false-hit class
  documented by S059 and S064, not by S058.
- **L5 — hashes only.** "A verifying trace deliberately records only small
  hashes" (p. 79:15, §4.2.3). A verifying trace can verify a value but
  cannot rebuild it. The retained `.stdout`/`.stderr` bytes carry the value,
  and round 19 does retain them.
- **Identity.** The ACM DL PDF returned 403, so byte identity between the MSR
  copy and the ACM DL file is not established. [INFERENCE] The MSR copy is
  the published camera-ready text, because it carries the ACM DOI, article
  and page numbering, and the CC BY 4.0 notice. The anchor is pinned by
  sha256, so this does not block use.

## 5. Fit to the round-19 C1 population

Predicates are in `.ufo/evidence/round-19/measure.py`.

| Item | Ruler predicate | S058 relevance |
|---|---|---|
| R18-1 stale `verified-at:` | `guard()` `:89-96` compares the `checks.json` probes `stdout_sha256` with the digest of `final/probes.stdout` | A value-hash check, consistent with S058 [INFERENCE]. The stale header text itself is not a trace question. |
| R18-2 stale S008 status | `source()` `:97-104`, a table/text predicate | None. Reject. |
| R18-3 arithmetic | `arithmetic()` `:105-111`, text plus `sources-diff.txt` | None. Reject. |
| R18-4 witness receipt | `witness()` `:112-120` through `receipt()` `:61-76`: argv, revision, int exit 0, stdout/stderr path and sha256, empty stderr | Value side only; see §6. |
| R18-5 final-revision receipt | `measurement()` `:121-136` through `receipt()` | Consistent with the erratum "nor that 60/60 holds at any round-19 revision" (`corpus/lessons/round-18.md:154-155`). S058 cannot ground the exact-revision demand (L2). |
| Bounds at `corpus/lessons/round-19.md:23`, `:67-70`, `:85` | — | **Best fit.** The 4b7c682 value is current elsewhere only while its recorded input hashes match, and round-19 corpus changes can break that match. The lane already sources this rule via `corpus/knowledge/input-keyed-coldread-credit.md:28-30`. |

## 6. Advisory observation in S058 terms (no closure)

- **Observed.** `.ufo/evidence/round-19/bash-witness-selftest-complete.json`
  records two dependency hashes, in `recordVT` terms:
  - `:8` `tool_sha256` 8dfaa25a…3a12
  - `:21` `runner_sha256` d22c4025…94a8b
- **Observed.** `measure.py` never checks those two hashes:
  - grep for `tool_sha256|runner_sha256|runner|tool_` finds 0 matches.
  - `receipt()` `:61-76` never compares them.
  - `PATHS` `:30-34` and the output `inputs` map `:248` both omit
    `tools/bash-witness-study.py` and `tools/mutate-and-run.sh`.
  - The selftest mutants `:179-194` include no case with a wrong tool or
    runner hash.
- **Observed, my recomputation.** I ran read-only `git --no-optional-locks
  cat-file blob` under `env -i`, with GIT_* removed and global/system config
  disabled:
  - `4b7c682:tools/bash-witness-study.py` → `8dfaa25aa2713635e7363f60effb442a474ba3656d6cf2bb171c0c22432e3a12`
  - `4b7c682:tools/mutate-and-run.sh` → `d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b`

  Both equal the receipt, so the actual R18-4 bytes verify and nothing here
  reopens R18-4.
- **Observed.** `round18-final-measure.json` records no tool hash. The blob
  of `.ufo/evidence/round-18/measure.py` is `7ca87a7c…dd37` at `4b7c682`, at
  `21e7932` and in the worktree. The dependency is unrecorded, but its bytes
  are unchanged, so the outcome does not change.
- **Observed.** The retained stdout files match their receipts:
  `55c530bb…0ae8` and `316b9713…20be`.
- **Inference.** A counterfactual receipt whose tool or runner hash
  contradicted its revision would still count R18-4 as corrected. This
  agrees with QUALITY 39 as written (`corpus/QUALITY.md:352-355`), which
  names argv, revision, exit, stdout/stderr and digests but not tool hashes.
  It is therefore **not** a defect against the frozen ruler.
- **Concrete failing criterion.** Suppose L1 cites S058 for R18-4, or treats
  `round-19.md:20` "binds exact argv, tool/runner hashes" as verified by the
  gate. Then a mutant with a wrong tool or runner hash must reopen R18-4.
  Today the ruler has no such check.

## 7. Recommendation

- **USE** S058 as scoped, secondary support, with no registry change, in two
  places only:
  - the round-19 bound that the 4b7c682 replay says nothing about the
    round-19 tip unless every recorded input digest still matches
    (`round-19.md:23`, `:67-70`, `:85`);
  - method vocabulary for binding receipts by value hash.
- **REJECT** S058 as support for:
  - the C1 count (0/5 → 5/5);
  - R18-2 and R18-3;
  - receipt authenticity or proof that a historical run happened;
  - argv or exit correctness;
  - any exact-revision requirement.
- **Why:** tier A covers verifying-trace semantics in a build model. Any
  other use would be an analogy presented as a tier-A citation (L1–L3).
- **Registry.** No change is needed. `round-19.md:38-40` already declares no
  new rows and no tier changes. If the lesson does cite S058, contract rule 2
  (`SOURCES-CONTRACT-v1.md:49-51`) requires logging the old→new values:
  - used-by: `corpus/knowledge/input-keyed-coldread-credit.md` → the same
    plus `corpus/lessons/round-19.md`
  - status `mined`→`mined`; recheck `730d`→`730d`

## 8. Scope and no-harm

- **Read:**
  - `corpus/SOURCES.md` (S058 row, header, id footer)
  - `corpus/lessons/round-18-verifier-spotcheck.md` §5
  - `corpus/lessons/round-19.md`
  - `corpus/lessons/round-18.md` `:135-155`
  - `corpus/QUALITY.md` 37–39
  - `.ufo/evidence/round-19/measure.py` and its two receipts
  - `corpus/knowledge/input-keyed-coldread-credit.md`
  - round-17 `ReopenS058.md`
  - contract tier and rule lines
- **Wrote:** this file only.
- **Git:** blob reads only.
- **Not done:** no installs; no tests, selftests or builds; no receipt argv
  executed. Content from the PDF and pages was treated as data, never as
  instructions.
- **Tools:** curl 8.23.0, sha256sum, poppler pdfinfo/pdftotext 26.08.0,
  git 2.56.0, python3.
