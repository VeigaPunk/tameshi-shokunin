#!/usr/bin/env python3
"""Re-locate every quoted span the pilot entry uses, in the bytes that were fetched.

Usage: quote-check.py QC.txt LIC.txt

  QC.txt   the `text` field of `aaron papers fetch 10.1145/351240.351266 --mode auto`
           (as fetched 2026-10-26; ligature losses and word splits preserved)
  LIC.txt  `pdftotext -layout lic.pdf` of https://smallbone.se/papers/lic.pdf
           (sha256 eaee48f930ba20a06824fe238cc6a42427e9fb45d1d70b852bf091ad6e44ac08)

Each span is de-spaced on both sides (the fetch splits words at random, e.g. `prop erties`)
and must occur exactly once. For S_QC the enclosing section is recovered from the fetched
markdown's own headers; for S_SB the PDF page and the printed page number at its top.
Exit 0 = every span located in the claimed place.
"""
import re
import sys

HRE = re.compile(r'^[ \t]*(?:#+[ \t]*)?(\d+\.?(?:\.\d+)*[ \t]+[A-Z][^\n]*?|[A-Z][A-Z ]{3,})[ \t]*$',
                 re.M)
SPANS = [
    ('S_QC', 'Abstract', "a to ol which aids the Haskell programmer in formulating and testing "
     "prop erties of programs. Prop erties are describ ed as Haskell functions, and can b e "
     "automatically tested on random input, but it is also p ossible to dene custom test data "
     "generators."),
    ('S_QC', '1', "it is meaningless to talk ab out random testing without discussing the "
     "distribution of test data"),
    ('S_QC', '1', "to put distribution under the h uman tester's con trol"),
    ('S_QC', '1', "a way to observe the distribution of test cases"),
    ('S_QC', '2.4', "it is worrying that very short lists dominate the test cases so strongly. "
     "After all, it is easy to de ne an erroneous version of insert which nevertheless works for "
     "lists with at most one element."),
    ('S_QC', '6.6', "The ma jor limitation of QuickCheck is that there is no measurement of test "
     "coverage: it is up to the user to investigate the distribution of test data"),
    ('S_QC', '3.2', "where the new parameter is to b e interpreted as some kind of size b ound"),
    ('S_QC', '3.2', "sized generates an a by passing the current size b ound to its parameter. It "
     "is then up to the programmer to interpret the size b ound in some reasonable way during test "
     "data generation."),
    ('S_QC', '7', "a novel way of controlling size when generating random elements of recursive "
     "data typ es."),
    ('S_SB', '2.10 p.34', "As always with random testing tools, the quality of the test data "
     "determines the quality of the generated equations. As such, it is important to provide good "
     "test data generators, that fit the program at hand."),
    ('S_SB', '2.10 p.34', "if we use an inappropriate generator"),
]


def despace(text):
    return re.sub(r'\s+', '', text)


def main(argv):
    if len(argv) != 3:
        print(__doc__.strip().splitlines()[0], file=sys.stderr)
        return 64
    qc = open(argv[1], encoding='utf-8', errors='replace').read()
    lic = open(argv[2], encoding='utf-8', errors='replace').read()
    qcflat, licflat = despace(qc), despace(lic)
    heads = [(m.start(), m.group(1).strip()) for m in HRE.finditer(qc)]
    pages = lic.split('\f')
    bad = 0
    for src, claim, span in SPANS:
        if src == 'S_QC':
            n = qcflat.count(despace(span))
            pattern = r'\s+'.join(re.escape(tok) for tok in span.split(' '))
            match = re.search(pattern, qc)
            off = match.start() if match else -1
            prior = [h for h in heads if h[0] <= off] if off >= 0 else []
            where = prior[-1][1] if prior else 'not-found'
            ok = n == 1 and where.lower().startswith(claim.lower())
        else:
            hits = [i for i, p in enumerate(pages, 1) if despace(span) in despace(p)]
            tops = [' '.join(pages[i - 1].split())[:2] for i in hits]
            n = len(hits)
            where = 'pdf_page=%s printed_top=%r' % (hits, tops)
            ok = n == 1 and tops == ['34']
        bad += 0 if ok else 1
        print('%-5s claim=%-10s count=%d %-46s %s'
              % (src, claim, n, where, 'OK' if ok else 'MISMATCH'))
    print('QUOTE_CHECK: spans=%d mismatched=%d' % (len(SPANS), bad))
    return 0 if bad == 0 else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
