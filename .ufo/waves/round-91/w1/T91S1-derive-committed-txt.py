#!/usr/bin/env python3
"""T91S1: byte-exact re-derivation of the frozen committed snapshot text.

Usage: T91S1-derive-committed-txt.py <input.html> <output.txt>

The frozen round-91 snapshot `.ufo/evidence/round-91/sources/git-env.txt` was NOT
produced by the round-90 stripper (`.ufo/waves/round-90/w1/T90S1-strip.py`,
which keeps <script>/<style> content and normalises whitespace per line).  This
recipe reproduces the committed file byte for byte:

  1. drop <script>...</script> and <style>...</style> blocks,
  2. replace every remaining tag with a single space,
  3. unescape HTML entities,
  4. collapse each run of horizontal whitespace to one space,
  5. split on newlines, drop lines that are blank after stripping,
  6. emit one leading line containing a single space, then the surviving lines
     verbatim (leading/trailing single spaces preserved), then a final newline.

Verified: `cmp` of the output against the frozen committed .txt is empty.
"""
import html
import re
import sys


def derive(raw: str) -> str:
    raw = re.sub(r"(?is)<script.*?</script>", "", raw)
    raw = re.sub(r"(?is)<style.*?</style>", "", raw)
    text = re.sub(r"(?s)<[^>]*>", " ", raw)
    text = html.unescape(text)
    text = re.sub(r"[ \t]+", " ", text)
    lines = [ln for ln in text.split("\n") if ln.strip()]
    return " \n" + "\n".join(lines) + "\n"


def main():
    src, dst = sys.argv[1], sys.argv[2]
    raw = open(src, encoding="utf-8", errors="replace").read()
    out = derive(raw)
    with open(dst, "w", encoding="utf-8") as fh:
        fh.write(out)
    print(f"{src} -> {dst}: {len(raw)} bytes raw, {out.count(chr(10))} text lines")


if __name__ == "__main__":
    main()
