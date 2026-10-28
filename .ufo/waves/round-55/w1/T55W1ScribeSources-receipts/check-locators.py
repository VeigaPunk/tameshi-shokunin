#!/usr/bin/env python3
"""Re-derive the byte offsets cited in T55W1ScribeSources.md from the committed
snapshots. Read-only. Run: python3 check-locators.py (from this directory)."""
import html
import re
import sys

HERE = __file__.rsplit("/", 1)[0] + "/sources/"

# (snapshot, raw byte offset claimed, raw bytes expected at that offset,
#  quote as rendered (whitespace-normalised), label)
ITEMS = [
    ("gnu-errors.html", 5020, b"Error messages from other noninteractive programs should look like this",
     "Error messages from other noninteractive programs should look like this:", "GNU noninteractive sentence"),
    ("gnu-errors.html", 5415, b'<var class="var">program</var>: <var class="var">message</var>',
     "program: message", "GNU second literal form (no source file)"),
    ("gnu-errors.html", 6247, b"<p>The string",
     "The string message should not begin with a capital letter when it follows a program name and/or file name",
     "GNU lowercase-after-program rule (var tags inside)"),
    ("gnu-errors.html", 6501, b"Also, it should not end with a period",
     "Also, it should not end with a period.", "GNU no-trailing-period rule"),
    ("sysexits.html", 49849, b"This interface has been",
     "This interface has been deprecated and is retained only for compatibility. Its use is discouraged.",
     "FreeBSD deprecation sentence"),
    ("sysexits.html", 53809, b"This interface is not portable",
     "This interface is not portable.", "FreeBSD BUGS non-portability"),
    ("sysexits.html", 53846, b"The choice of an appropriate exit value",
     "The choice of an appropriate exit value is often ambiguous.", "FreeBSD BUGS ambiguity"),
    ("gnu-errors.html", 5154, b'<var class="var">program</var>:<var class="var">sourcefile</var>',
     "program:sourcefile:lineno: message", "GNU first literal form (with a source file)"),
    ("gnu-errors.html", 204, b"last updated April 27, 2026",
     "last updated April 27, 2026", "GNU Coding Standards revision stamp"),
    ("sysexits.html", 50084, b"Error\n     numbers begin at",
     "Error numbers begin at EX__BASE to reduce the possibility of clashing with other exit statuses that random programs may already return.",
     "FreeBSD EX__BASE clash-avoidance sentence"),
    ("sysexits.html", 50240, b"The meaning of the",
     "The meaning of the codes is approximately as follows:", "FreeBSD approximate-codes sentence"),
]


def normalise(raw: bytes, sep: str = "") -> str:
    """Inline HTML tags add no space, so strip them with '' first; the ' ' form
    is kept as a fallback for quotes that sit beside a block boundary."""
    text = re.sub(r"<[^>]+>", sep, raw.decode("utf-8", "replace"))
    text = html.unescape(text)
    text = text.replace("\u00a0", " ")
    return re.sub(r"\s+", " ", text).strip()


def main() -> int:
    bad = 0
    for snap, off, expect_raw, quote, label in ITEMS:
        raw = open(HERE + snap, "rb").read()
        at = raw[off:off + len(expect_raw)]
        raw_ok = at == expect_raw
        norm_ok = quote in normalise(raw) or quote in normalise(raw, ' ')
        if snap == "gnu-errors.html" and off == 204:
            norm_ok = True  # revision stamp sits inside an HTML comment; raw bytes only
        words = len(quote.split())
        status = "OK" if (raw_ok and norm_ok and words <= 25) else "FAIL"
        if status == "FAIL":
            bad += 1
        print(f"{status:4} {snap}:{off} words={words:2} raw={raw_ok} rendered={norm_ok}  {label}")
        if not raw_ok:
            print(f"     expected {expect_raw!r}\n     found    {at!r}")
    # the same-file statement that grounds the scope limit of the GNU row
    gnu = normalise(open(HERE + "gnu-errors.html", "rb").read())
    print(f"GNU page mentions 'exit': {'exit' in gnu.lower()} (scope limit: line shape only)")
    idx = normalise(open(HERE + "gnu-node-index.html", "rb").read()).lower()
    print(f"GNU standards node index has an exit/status node: "
          f"{bool(re.search(r'exit|status', idx))}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
