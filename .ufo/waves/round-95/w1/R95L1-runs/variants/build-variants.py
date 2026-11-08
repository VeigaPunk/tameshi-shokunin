#!/usr/bin/env python3
"""Build the five round-95 single-fix counter variants from the v94 bytes.

Reads base/measure-v94.py (extracted from the lane object store at the round
base), applies exactly one parser fix per variant plus the combined variant,
and recomputes SELF_SHA256 for each result (strip the single pin line, sha256
the rest, write it back). The four fix texts follow R95E1's frozen instruction
list verbatim in mechanics; only the round-95 paths/labels are NOT applied, so
every variant still runs against the round-94 spec at the round base.
"""
import difflib
import hashlib
import os
import re
import subprocess
import sys

S = sys.argv[1]
BASE = os.path.join(S, "base", "measure-v94.py")
OUT = os.path.join(S, "variants")
PIN_RE = re.compile(rb'^SELF_SHA256 = "[0-9a-f]{64}"\n', re.M)

BLOCK_FN = r'''def block_lines(text):
    """(orig_index, text) for every line outside a fenced code block (S322).

    Round-95 A2: a line matching `^ {4,}\S` is a literal indented-code line
    and is not visible, unless it continues a list item. `list_open` is set by
    a visible non-blank list-marker line, survives blank lines, and closes on a
    visible non-indented non-marker line.
    """
    list_item = re.compile(r"^ {0,3}(?:[-*+]|\d{1,9}[.)])\s")
    indented = re.compile(r"^ {4,}\S")
    vis, fence, list_open = [], None, False
    for idx, raw in enumerate(text.split("\n")):
        m = FENCE_RE.match(raw)
        if fence is None:
            if m:
                fence = (m.group(1)[0], len(m.group(1)))
                continue
            if raw.strip() == "":
                vis.append((idx, raw))
                continue
            if list_item.match(raw):
                list_open = True
            elif indented.match(raw):
                if not list_open:
                    continue
            else:
                list_open = False
            vis.append((idx, raw))
        else:
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= fence[1] \
                    and m.group(2).strip() == "":
                fence = None
            continue
    return vis'''

CELLS_FN = r'''def split_cells(line):
    """GFM cell split: unescaped `|` separates cells; `\|` is a literal pipe.

    Round-95 A4: `\\` is a literal backslash and is handled before `\|`, so a
    cell ending in a literal backslash closes at the following `|`.
    """
    out, cur, i = [], [], 0
    while i < len(line):
        ch = line[i]
        if ch == "\\" and i + 1 < len(line) and line[i + 1] == "\\":
            cur.append("\\")
            i += 2
            continue
        if ch == "\\" and i + 1 < len(line) and line[i + 1] == "|":
            cur.append("|")
            i += 2
            continue
        if ch == "|":
            out.append("".join(cur).strip())
            cur = []
            i += 1
            continue
        cur.append(ch)
        i += 1
    out.append("".join(cur).strip())
    if out and out[0] == "":
        out = out[1:]
    if out and out[-1] == "":
        out = out[:-1]
    return out'''

PIN_FN = r'''def self_pin_state():
    """QUALITY 150 + round-95 A3: exactly one pin line, then the digest.

    The check runs before any other action, on the file's own bytes. A second
    pin line is a setup refusal (`self-pin-line-count`), not a stripped no-op.
    """
    try:
        with open(os.path.abspath(__file__), "rb") as f:
            b = f.read()
    except OSError:
        return "self-pin-mismatch"
    if len(re.findall(SELF_PIN_RE, b, flags=re.M)) != 1:
        return "self-pin-line-count"
    norm = re.sub(SELF_PIN_RE, b"", b, flags=re.M)
    if hashlib.sha256(norm).hexdigest() != SELF_SHA256:
        return "self-pin-mismatch"
    return "ok"'''

def _delim_line_fix(src):
    """Replace -{3,} with -{1,} on the single DELIM_RE line."""
    lines = src.split("\n")
    hits = [i for i, l in enumerate(lines) if l.startswith("DELIM_RE = re.compile(")]
    assert len(hits) == 1, hits
    i = hits[0]
    assert lines[i].count("-{3,}") == 2, lines[i]
    lines[i] = lines[i].replace("-{3,}", "-{1,}")
    return "\n".join(lines)

CONJ_OLD = '''    if "--conjuncts" in sys.argv:
        if not self_pin_ok():
            die("self-pin-mismatch")'''
CONJ_NEW = '''    if "--conjuncts" in sys.argv:
        _pin_state = self_pin_state()
        if _pin_state != "ok":
            die(_pin_state)'''

MAIN_OLD = '''    selfpin = self_pin_ok()
    if not selfpin:
        die("self-pin-mismatch")'''
MAIN_NEW = '''    _pin_state = self_pin_state()
    selfpin = _pin_state == "ok"
    if not selfpin:
        die(_pin_state)'''


def replace_block(src, name, new):
    lines = src.split("\n")
    starts = [i for i, l in enumerate(lines) if l.startswith("def %s(" % name)]
    assert len(starts) == 1, (name, starts)
    i = starts[0]
    js = [k for k in range(i + 1, len(lines)) if lines[k].startswith("def ")]
    assert js, name
    j = js[0]
    block = lines[i:j]
    trailing = 0
    while trailing < len(block) and block[len(block) - 1 - trailing] == "":
        trailing += 1
    lines[i:j] = new.split("\n") + [""] * trailing
    return "\n".join(lines)


def replace_once(src, old, new):
    n = src.count(old)
    assert n == 1, (n, old[:60])
    return src.replace(old, new, 1)


def repin(text):
    b = text.encode()
    pins = PIN_RE.findall(b)
    assert len(pins) == 1, len(pins)
    digest = hashlib.sha256(PIN_RE.sub(b"", b)).hexdigest()
    out = PIN_RE.sub(('SELF_SHA256 = "%s"\n' % digest).encode(), b)
    return out.decode(), digest


def fix_indent(src):
    return replace_block(src, "block_lines", BLOCK_FN)


def fix_cells(src):
    return replace_block(src, "split_cells", CELLS_FN)


def fix_delim(src):
    return _delim_line_fix(src)


def fix_pin(src):
    src = replace_block(src, "self_pin_ok", PIN_FN)
    src = replace_once(src, CONJ_OLD, CONJ_NEW)
    src = replace_once(src, MAIN_OLD, MAIN_NEW)
    return src


VARIANTS = [
    ("fix-indent-code", [fix_indent]),
    ("fix-split-cells", [fix_cells]),
    ("fix-delimiter", [fix_delim]),
    ("fix-single-pin", [fix_pin]),
    ("fix-combined", [fix_indent, fix_cells, fix_delim, fix_pin]),
]


def main():
    src0 = open(BASE, "rb").read().decode()
    assert hashlib.sha256(src0.encode()).hexdigest() == \
        "a22563b0c2b4a2b43922cec3d1ab3fa511110e035b9edfdfdc6eaebb97023010"
    os.makedirs(OUT, exist_ok=True)
    manifest = {}
    for name, fns in VARIANTS:
        src = src0
        for fn in fns:
            src = fn(src)
        out, digest = repin(src)
        path = os.path.join(OUT, name + ".py")
        with open(path, "w", encoding="utf-8") as f:
            f.write(out)
        os.chmod(path, 0o755)
        diff = "".join(difflib.unified_diff(
            src0.splitlines(True), out.splitlines(True),
            fromfile="base/measure-v94.py", tofile=name + ".py"))
        with open(os.path.join(OUT, name + ".diff"), "w", encoding="utf-8") as f:
            f.write(diff)
        p = subprocess.run([sys.executable, "-I", path, "--conjuncts"],
                           capture_output=True, text=True)
        manifest[name] = dict(sha256=hashlib.sha256(out.encode()).hexdigest(),
                              self_pin=digest, conjuncts_rc=p.returncode,
                              conjuncts=p.stdout.strip().replace("\n", " | "))
        print("%-16s rc=%d %s" % (name, p.returncode,
                                  p.stdout.strip().replace("\n", " | ")))
        assert p.returncode == 0, p.stderr
        assert "C1_R94_PASS=keys-only" in p.stdout
    # witness: the combined variant refuses a second pin line and one edited byte.
    comb = os.path.join(OUT, "fix-combined.py")
    text = open(comb, encoding="utf-8").read()
    second = text.replace(
        '\n\nif __name__ == "__main__":',
        '\nSELF_SHA256 = "%s"\n\nif __name__ == "__main__":' % ("0" * 64), 1)
    pin_lines = re.findall(r'^SELF_SHA256 = "[0-9a-f]{64}"$', second, flags=re.M)
    assert second != text and len(pin_lines) == 2, len(pin_lines)
    p1 = os.path.join(OUT, "witness-double-pin.py")
    open(p1, "w", encoding="utf-8").write(second)
    r1 = subprocess.run([sys.executable, "-I", p1, "--conjuncts"],
                        capture_output=True, text=True)
    edited = text.replace('print("C1_CONJUNCT_KEYS ', 'print("C1_CONJUNCT_KEYS  ', 1)
    assert edited != text
    p2 = os.path.join(OUT, "witness-byte-edit.py")
    open(p2, "w", encoding="utf-8").write(edited)
    r2 = subprocess.run([sys.executable, "-I", p2, "--conjuncts"],
                        capture_output=True, text=True)
    print("witness-double-pin rc=%d %s" % (r1.returncode,
                                           r1.stdout.strip().replace("\n", " | ")))
    print("witness-byte-edit  rc=%d %s" % (r2.returncode,
                                           r2.stdout.strip().replace("\n", " | ")))
    assert r1.returncode == 2 and "C1_SETUP self-pin-line-count" in r1.stdout
    assert r2.returncode == 2 and "C1_SETUP self-pin-mismatch" in r2.stdout
    with open(os.path.join(OUT, "manifest.txt"), "w", encoding="utf-8") as f:
        for k, v in manifest.items():
            f.write("%s sha256=%s self_pin=%s conjuncts_rc=%d\n" % (
                k, v["sha256"], v["self_pin"], v["conjuncts_rc"]))
        f.write("witness-double-pin rc=%d\n" % r1.returncode)
        f.write("witness-byte-edit rc=%d\n" % r2.returncode)
    return 0


if __name__ == "__main__":
    sys.exit(main())
