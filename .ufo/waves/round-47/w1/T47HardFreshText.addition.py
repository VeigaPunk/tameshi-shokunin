"""Round-47 C2 seat T47HardFreshText: named cases for extract(), words(), grade() and review_sets().

Five rule-level cases (FT01-FT05) plus two review cases (FT06-FT07), each the smallest
behavioural fixture that separates the pristine round-46 hardened freshness counter from a
mutant this seat owns. No case reads the counter's own source, hashes it or pins a length, so
the neutral (commute) mutants and CTL_E are untouched.

  FT01 extract:PDF branch      a raw blob that starts with %PDF must go through pdftotext.
                               `raw[:4]` -> `raw[:5]` (extract:int:0) skips the branch and
                               decodes the PDF bytes, so the extracted text disappears and
                               `%PDF` shows up; `capture_output=True` -> `False`
                               (extract:const:0) leaves `out.stdout` None and the call raises
                               AttributeError, which this case reports as a named FAIL.
                               pdftotext is a PATH-first shell stub printing one fixed line
                               (the brief's fake-curl pattern): no PDF tool, no network.
  FT02 words stop-word filter   `and` -> `or` (words:bool:0) keeps short words and stopwords.
  FT03 words minimum length 4   `>=` -> `>` (words:cmp:0) and `4` -> `5` (words:int:0) drop a
                               4-letter content word; pristine keeps it.
  FT04 grade overlap floor 2    a 6..25-token quote present in the page with EXACTLY 2 content
                               words shared with scope+anchor+teaches: `< 2` -> `<= 2`
                               (grade:cmp:9) and `2` -> `3` (grade:int:0) both refuse it.
  FT05 grade quote upper 25     a 25-token quote (the bound itself) must be admitted;
                               `n > 25` -> `n >= 25` (grade:cmp:11) refuses it as length 25.
  FT06/FT07 review_sets gates   FT06: an independent agree whose report names id and reviewer
                               is admitted (the `not text` deletion, review_sets:not:2, makes
                               every non-empty report skip, so nothing is admitted).
                               FT07: a report naming the id but NOT the reviewer is refused
                               (`or` -> `and` on line 209, review_sets:bool:1, admits it).

Why an import-time tripwire covers FT06/FT07 only
-------------------------------------------------
The round-46 selftest calls review_sets() inside selftest() itself (the T17 block), before any
`extra_*()` -- the assembler appends the extra calls only before the tally print. Both mutants
above make that T17 call site raise (T17 feeds a review whose report is absent, so `text` is
None; `not text` is then evaluated against `re.search(..., None)`), so the run ends as a
traceback with no named FAIL and a later case could never report them. The tripwire below runs
the same two fixtures at import time, prints ONLY named `FAIL` lines (nothing when both hold),
and does nothing outside `--selftest`, so the pristine counter and the --lane/--check/--live
modes print no additional bytes. FT01-FT05 need no tripwire: their mutants do not raise in any
earlier selftest case.
"""

import shutil

_PDF_RAW = (b'%PDF-1.7\n%\xe2\xe3\xcf\xd3\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\n'
            b'endobj\ntrailer\n<< /Root 1 0 R >>\nstartxref\n0\n%%EOF\n')
_PDF_TEXT = 'Portable document marker sentence inside the extracted body'

# 11 tokens, present in _PAGE_OVERLAP2, sharing exactly {flaky, cluster} with _xHardGrade_row().
_QUOTE_OVERLAP2 = 'Ordering hides flaky runs while the cluster appears only after reruns'
_PAGE_OVERLAP2 = ('<html><body><p>' + _QUOTE_OVERLAP2 + '.</p></body></html>').encode('utf-8')

# 25 whitespace tokens (the upper bound itself), verbatim inside _xHardGrade_page().
_QUOTE_25 = ('Flaky failures cluster inside the same job because the rerun repeats one order of '
             'the tests only and the second attempt hides the ordering defect')

_REVIEW_REPORT = '.ufo/waves/round-45/w2/T47Text.md'
_REVIEW_CTL = '.ufo/waves/round-45/w2/T47TextCtl.md'


def _xT47HardFreshText_pdf_dir():
    """A PATH-first `pdftotext` stub that prints _PDF_TEXT and ignores its arguments."""
    d = tempfile.mkdtemp(prefix='tameshi-r47-t47text-')
    p = os.path.join(d, 'pdftotext')
    with open(p, 'w', encoding='utf-8') as fh:
        fh.write("#!/bin/sh\nprintf '%s\\n' '" + _PDF_TEXT + "'\n")
    os.chmod(p, 0o755)
    return d


def _xT47HardFreshText_extract_pdf():
    """(ok, detail): the PDF branch must return pdftotext's text, not the decoded raw bytes."""
    d = _xT47HardFreshText_pdf_dir()
    saved = os.environ.get('PATH', '')
    os.environ['PATH'] = d + (os.pathsep + saved if saved else '')
    try:
        try:
            got = extract(_PDF_RAW)
        except Exception as exc:  # capture_output=False -> out.stdout is None -> AttributeError
            got = '<raised %s>' % type(exc).__name__
    finally:
        os.environ['PATH'] = saved
        shutil.rmtree(d, ignore_errors=True)
    ok = _PDF_TEXT in got and '%PDF' not in got
    return ok, 'text=%r' % (got[:60],)


def _xT47HardFreshText_entry(quote, raw):
    row = _xHardGrade_row()
    return dict(id=row['id'], url=row['url'], opened='2026-10-25', verdict='holds',
                raw_sha256=hashlib.sha256(raw).hexdigest(), quote=quote)


def _xT47HardFreshText_grade_cases():
    """(name, ok, detail) for the two grade() thresholds: overlap floor 2, quote length 25."""
    row = _xHardGrade_row()
    out = []
    got = grade(_xT47HardFreshText_entry(_QUOTE_OVERLAP2, _PAGE_OVERLAP2), row, _PAGE_OVERLAP2)
    out.append(('FT04_grade_overlap_two_admitted', got == ('verified', 'ok'), '%r' % (got,)))
    page = _xHardGrade_page()
    got = grade(_xT47HardFreshText_entry(_QUOTE_25, page), row, page)
    out.append(('FT05_grade_quote_25_admitted', got == ('verified', 'ok'), '%r' % (got,)))
    return out


def _xT47HardFreshText_words_cases():
    """(name, ok, detail): the stop-word filter and the length-4 floor of words()."""
    out = []
    got = sorted(words('that alpha'))
    out.append(('FT02_words_stopword_excluded', got == ['alpha'], '%r' % (got,)))
    got = sorted(words('quad alpha'))
    out.append(('FT03_words_min_length_four', got == ['alpha', 'quad'], '%r' % (got,)))
    return out


def _xT47HardFreshText_review_run():
    """(name, ok, detail) for the two report-text gates of review_sets().

    One refused review (report names the id, not the reviewer) and one admitted control
    (report names both), so a gate that stops counting everything fails FT06 too.
    """
    seats = wave_seats(json.dumps({'results': [
        {'name': 'RevT47', 'output': 'done'}, {'name': 'RevT47Ctl', 'output': 'done'}]}))
    authors = {'S001': 'ExecT47', 'S002': 'ExecT47'}
    reports = {_REVIEW_REPORT: 'S001 was re-checked against the ledger by an independent seat',
               _REVIEW_CTL: 'RevT47Ctl re-checked S002 and agrees'}
    reviews = [dict(id='S001', reviewer='RevT47', verdict='agree', report=_REVIEW_REPORT),
               dict(id='S002', reviewer='RevT47Ctl', verdict='agree', report=_REVIEW_CTL)]
    agreed, disputed = review_sets({'S001', 'S002'}, reviews, authors, reports.get, seats)
    out = [('FT06_review_control_admitted', 'S002' in agreed and not disputed, 'agreed=%s' % sorted(agreed)),
           ('FT07_review_report_names_reviewer', 'S001' not in agreed, 'agreed=%s' % sorted(agreed))]
    return out


def _xT47HardFreshText_run():
    """(name, ok, detail) for every case, in a stable order."""
    ok, detail = _xT47HardFreshText_extract_pdf()
    out = [('FT01_extract_pdf_branch', ok, detail)]
    out += _xT47HardFreshText_words_cases()
    out += _xT47HardFreshText_grade_cases()
    out += _xT47HardFreshText_review_run()
    return out


def _xT47HardFreshText_tripwire():
    """Pre-selftest named case for the two review_sets() mutants whose crash precedes every extra_*()."""
    if '--selftest' not in sys.argv:
        return 0
    try:
        results = _xT47HardFreshText_review_run()
    except Exception:
        return 0
    bad = 0
    for name, ok, detail in results:
        if not ok:
            bad += 1
            print('FAIL %s early %s' % (name, detail))
    return bad


_XT47HardFreshText_EARLY = _xT47HardFreshText_tripwire()


def extra_T47HardFreshText():
    """Return (cases, failed): the extract/words/grade/review_sets cases of this seat."""
    cases = failed = 0
    for name, ok, detail in _xT47HardFreshText_run():
        cases += 1
        failed += not ok
        print('%s %s %s' % ('PASS' if ok else 'FAIL', name, detail))
    return cases, failed
