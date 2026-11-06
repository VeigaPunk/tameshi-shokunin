#!/usr/bin/env python3
"""T89S1-quote-locate.py — round-89 seat T89S1 (scout), READ-ONLY source reconnaissance.

Locates four quotes in a TAG-STRIPPED text of two live man7 pages and reports, for each
quote: the tag-stripped line span, the raw-HTML line span, the whitespace-token word
count of the quote AS GIVEN (the rule the lane corrected in round-86 M5: the token count
of the quoted string itself, not of the source line it sits on), and the sha256 of the
live page vs the committed snapshot.

Tag-strip rule (deterministic, disclosed):
  1. remove HTML comments <!-- ... --> (may span lines)
  2. remove <script>...</script> and <style>...</style> blocks (may span lines)
  3. remove every remaining tag <...> (never spans lines)
  4. unescape HTML entities; replace U+00A0 with U+0020
  5. split on '\n'  -- one stripped line per source line, except where a multi-line
     comment/script/style block was removed (those lines vanish)

Usage: python3 T89S1-quote-locate.py <live-execve.html> <live-strace.html>
Exit:  0 all four quotes located, 1 a quote was not located.
"""
import hashlib
import html
import re
import sys

QUOTES = [
    ("Q1", "many attributes of the calling process remain unchanged (in particular, its PID)", "execve"),
    ("Q2", "By default, file descriptors remain open across an execve().", "execve"),
    ("Q3", "Prints paths associated with file descriptor arguments and with the AT_FDCWD constant.", "strace"),
    ("Q4", "Prints unabbreviated versions of environment, stat, termios, etc. calls.", "strace"),
]


def strip_lines(path):
    raw = open(path, encoding="utf-8", errors="replace").read()
    s = re.sub(r"(?s)<!--.*?-->", "", raw)
    s = re.sub(r"(?s)<script.*?</script>", "", s)
    s = re.sub(r"(?s)<style.*?</style>", "", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s).replace("\xa0", " ")
    return s.split("\n"), raw.split("\n"), hashlib.sha256(raw.encode()).hexdigest()


def locate(lines, quote):
    segs, pos = [], 0
    for i, l in enumerate(lines):
        s = " ".join(l.split())
        if not s:
            continue
        segs.append((i + 1, s, pos))
        pos += len(s) + 1
    flat = " ".join(s for _, s, _ in segs)
    j = flat.find(quote)
    if j < 0:
        return None
    j2 = j + len(quote)
    covered = [(ln, s) for ln, s, p in segs if p < j2 and p + len(s) >= j]
    return covered, " ".join(s for _, s in covered)


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    ex, st = sys.argv[1], sys.argv[2]
    pages = {}
    for tag, path in (("execve", ex), ("strace", st)):
        lines, raw, digest = strip_lines(path)
        pages[tag] = (lines, raw, digest)
        print(f"PAGE {tag}: {path}")
        print(f"  sha256(live)   = {digest}")
        print(f"  raw html lines = {len(raw)}   tag-stripped lines = {len(lines)}")
    bad = 0
    for name, q, which in QUOTES:
        lines, raw, _ = pages[which]
        res = locate(lines, q)
        if res is None:
            print(f"{name}: NOT LOCATED")
            bad += 1
            continue
        covered, span = res
        raw_hits = [i + 1 for i, l in enumerate(raw)
                    if q[:40] in " ".join(re.sub(r"<[^>]+>", "", html.unescape(l)).split())]
        raw_span = [i + 1 for i, l in enumerate(raw)
                    if span[:40] in " ".join(re.sub(r"<[^>]+>", "", html.unescape(l)).split())]
        print(f"{name}: {' '.join(w for w in [q])}")
        print(f"  tag-stripped lines {covered[0][0]}-{covered[-1][0]}")
        for ln, s in covered:
            print(f"    {ln}| {s}")
        print(f"  raw-html line(s) {raw_hits}")
        print(f"  quote word count (whitespace tokens of the quote as given) = {len(q.split())}")
        print(f"  quote appears verbatim in the joined stripped text: {span.strip() == q}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
