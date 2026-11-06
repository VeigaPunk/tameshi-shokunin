#!/usr/bin/env python3
"""T90S1: tag-strip an HTML page to a line-per-block text file.

Usage: strip.py <input.html> <output.txt>

The strip is deterministic: html.parser collects character data; a newline is
inserted at the start and end of every block-level element (p, div, li, h1-h6,
pre, tr, table, blockquote, dt, dd, br); entities are unescaped; blank lines
are dropped. Line numbers quoted in T90S1.md refer to the output file.
"""
import html
import html.parser
import sys

BLOCKS = {"p", "div", "li", "h1", "h2", "h3", "h4", "h5", "h6", "pre",
          "tr", "table", "blockquote", "dt", "dd", "br", "hr", "section"}


class Stripper(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in BLOCKS:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in BLOCKS:
            self.parts.append("\n")

    def handle_data(self, data):
        self.parts.append(data)

    def handle_entityref(self, name):
        self.parts.append("&" + name + ";")

    def handle_charref(self, name):
        self.parts.append("&#" + name + ";")


def main():
    src, dst = sys.argv[1], sys.argv[2]
    raw = open(src, encoding="utf-8", errors="replace").read()
    p = Stripper()
    p.feed(raw)
    p.close()
    text = html.unescape("".join(p.parts))
    lines = [ln.strip() for ln in text.split("\n")]
    lines = [ln for ln in lines if ln]
    with open(dst, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"{src} -> {dst}: {len(raw)} bytes raw, {len(lines)} text lines")


if __name__ == "__main__":
    main()
