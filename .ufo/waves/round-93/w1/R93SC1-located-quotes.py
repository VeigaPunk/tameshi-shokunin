#!/usr/bin/env python3
"""R93SC1 probe: the located quotes the frozen counter's `source` conjunct accepts.

Reads the lesson and the three source snapshots at the instrument revision
855f0c1c59ee2af7f184d8de62d02cdd576eb94e and reports, per source id, the
quoted spans of at most 25 words that sit on a line naming that id AND occur
in the committed snapshot (the rule the counter implements in
located_quotes()/norm_text()).

Read-only: every byte comes from `git cat-file`; nothing is written.
"""
import hashlib
import html as htmlmod
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
REV = "855f0c1c59ee2af7f184d8de62d02cdd576eb94e"
LESSON = "corpus/lessons/round-93.md"
SOURCE_ROWS = {
    "S320": ".ufo/evidence/round-93/sources/s320.html",
    "S321": ".ufo/evidence/round-93/sources/s321.html",
    "S322": ".ufo/evidence/round-93/sources/s322.html",
}


def blob(path):
    p = subprocess.run(["git", "-C", LANE, "cat-file", "blob", "%s:%s" % (REV, path)],
                       capture_output=True)
    if p.returncode != 0:
        return None
    return p.stdout


def norm_text(s):
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    s = htmlmod.unescape(s)
    s = s.replace("\u2019", "'").replace("\u2018", "'")
    s = s.replace("\u201c", '"').replace("\u201d", '"')
    s = s.replace("\u2014", "-").replace("\u2013", "-").replace("\u00a0", " ")
    return re.sub(r"\s+", " ", s).strip()


def located_quotes(lesson_text):
    out = {sid: [] for sid in SOURCE_ROWS}
    for line in lesson_text.split("\n"):
        quoted = re.findall(r'"([^"\n]{3,300})"', line)
        if not quoted:
            continue
        for sid in SOURCE_ROWS:
            if sid in line:
                for q in quoted:
                    if 1 <= len(q.split()) <= 25:
                        out[sid].append(q)
    return out


def main():
    lesson_b = blob(LESSON)
    if lesson_b is None:
        print("LESSON_ABSENT")
        return 2
    lesson = lesson_b.decode("utf-8", errors="replace")
    quotes = located_quotes(lesson)
    for sid, snap in SOURCE_ROWS.items():
        snap_b = blob(snap)
        if snap_b is None:
            print("%s SNAPSHOT_ABSENT %s" % (sid, snap))
            continue
        text = norm_text(snap_b.decode("utf-8", errors="replace"))
        accepted = [q for q in quotes.get(sid, []) if norm_text(q) in text]
        print("%s snapshot=%s sha256=%s" % (sid, snap,
              hashlib.sha256(snap_b).hexdigest()[:16]))
        for q in quotes.get(sid, []):
            ok = norm_text(q) in text
            print("   %s words=%d %s" % ("ACCEPTED" if ok else "rejected",
                                         len(q.split()), q[:110]))
        print("   accepted_count=%d" % len(accepted))
    return 0


if __name__ == "__main__":
    sys.exit(main())
