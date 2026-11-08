#!/usr/bin/env python3
"""T92C1 attack driver — kill attempt against R92-C1 under its own kill rule (a).

For each attempt: fresh `git clone --shared` of the lane at instrument rev
84904d41, one commit holding the mutated note/README/lesson bytes (identity
ctl <ctl@fixture.invalid>), then the FROZEN counter bytes (sha256
be5a9221..., extracted from 84904d41 and re-verified here) run at that
commit.  Prints one line per attempt and writes the full counter transcript.

Nothing in /home/vgpnk/Projects/shokunin is written except the w1 deliverable
directory passed with --out.
"""
import hashlib, json, os, re, shutil, subprocess, sys, concurrent.futures as cf

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
REV = "84904d41a31fb5ddde49e8bf1ad6fc2b489671a0"
SUM = "a6adf4a6c89feb35f8633a2942c0bfcd729aa3ccbdc57e10fef98ce9b8cc2fe3"
NOTE = "corpus/knowledge/mutation-case-fleet-sources-census.md"
README = "corpus/README.md"
LESSON = "corpus/lessons/round-92.md"
SPECDIR = ".ufo/evidence/round-92/c1"

TRUE = {"C01": "KILLED", "C02": "SURVIVED", "C03": "SURVIVED", "C04": "KILLED",
        "C05": "KILLED", "C06": "SURVIVED", "C07": "KILLED", "C08": "SURVIVED",
        "C09": "SURVIVED", "C10": "SURVIVED", "C11": "KILLED", "C12": "SURVIVED"}
FLIP = {k: ("SURVIVED" if v == "KILLED" else "KILLED") for k, v in TRUE.items()}


def git(repo, *a, check=True, identity=False):
    cmd = ["git", "-C", repo]
    if identity:
        cmd += ["-c", "user.name=ctl", "-c", "user.email=ctl@fixture.invalid"]
        cmd += ["-c", "commit.gpgsign=false"]
    return subprocess.run(cmd + list(a), capture_output=True, text=True, check=check)


def show(rev, path):
    return git(LANE, "cat-file", "blob", f"{rev}:{path}").stdout


def inv_table(lang=""):
    lines = ["| id | arm targeted | edit | verdict | witness |", "|---|---|---|---|---|"]
    lines += ["| %s | arm | edit | %s | witness |" % (k, FLIP[k]) for k in TRUE]
    return "\n".join(lines)


def html_table():
    rows = "\n".join("<tr><td>%s</td><td>arm</td><td>%s</td></tr>" % (k, FLIP[k]) for k in TRUE)
    return ("<table>\n<tr><th>id</th><th>arm targeted</th><th>verdict</th></tr>\n"
            + rows + "\n</table>")


def edit_row_cell(text, rid, col, newval):
    out = []
    for line in text.split("\n"):
        cells = line.split("|")
        if len(cells) > col and cells[1].strip() == rid:
            cells[col] = newval
            line = "|".join(cells)
        out.append(line)
    return "\n".join(out)


# ---- note transforms: (name, description, fn(note, extra) -> (note, extra)) ----
def a_fenced(note, extra):
    return note.rstrip("\n") + "\n\n```\n" + inv_table() + "\n```\n", extra


def a_html(note, extra):
    return note.rstrip("\n") + "\n\n" + html_table() + "\n", extra


def a_prose(note, extra):
    prose = ("In summary the twelve cells read: " +
             ", ".join("%s %s" % (k, FLIP[k]) for k in TRUE) + ".")
    return note.rstrip("\n") + "\n\n" + prose + "\n", extra


def a_escaped(note, extra):
    rows = []
    for line in note.split("\n"):
        cells = line.split("|")
        if len(cells) > 3 and cells[1].strip() == "C01":
            cells[3] = ' `kind=="community" \\| "communityX"` '
            line = "|".join(cells)
        rows.append(line)
    return "\n".join(rows), extra


def a_dupheader(note, extra):
    hdr = "| id | arm targeted | edit | verdict | witness |"
    rows = []
    for line in note.split("\n"):
        if line.startswith("| C02 |"):
            rows.append(hdr)
        rows.append(line)
    return "\n".join(rows), extra


def a_drop(note, extra):
    return "\n".join(l for l in note.split("\n") if not l.startswith("| C12 |")), extra


def a_measured_fence(note, extra):
    return note.rstrip("\n") + "\n\n```\nmeasured: 7/12 killed\n```\n", extra


def a_bold_ids(note, extra):
    out = []
    for line in note.split("\n"):
        cells = line.split("|")
        if len(cells) > 3 and re.fullmatch(r"C\d\d", cells[1].strip()):
            cells[1] = " **%s** " % cells[1].strip()
            line = "|".join(cells)
        out.append(line)
    return "\n".join(out), extra


def a_backtick_verdict(note, extra):
    out = []
    for line in note.split("\n"):
        cells = line.split("|")
        if len(cells) > 4 and re.fullmatch(r"C\d\d", cells[1].strip()) and cells[4].strip() == TRUE[cells[1].strip()]:
            cells[4] = " `%s` " % cells[4].strip()
            line = "|".join(cells)
        out.append(line)
    return "\n".join(out), extra


def a_coverage_decoy(note, extra):
    # remove the Core coverage row that names the note; the round-91 "not
    # admitted" row (which also names it) stays and is the decoy.
    rl = extra[README].split("\n")
    extra[README] = "\n".join(l for l in rl
                              if not (l.lstrip().startswith("|") and
                                      "knowledge/mutation-case-fleet-sources-census.md" in l
                                      and "not admitted" not in l))
    return note, extra


def a_source_decoy(note, extra):
    # keep S320 `mined` but strip every substantive grounding from the lesson
    # paragraph, leaving only the id and the URL as bare tokens.
    ls = extra[LESSON]
    out, hit = [], 0
    for line in ls.split("\n"):
        if "S320" in line and "sha256sum.1.en" in line:
            out.append("S320 https://man.archlinux.org/man/sha256sum.1.en")
            hit += 1
        else:
            out.append(line)
    print("    source-decoy lines replaced:", hit, file=sys.stderr)
    extra[LESSON] = "\n".join(out)
    return note, extra


def a_idkeyed_impact(note, extra):
    # a second table keyed by the spec ids in its first column, no verdict
    # tokens at all -- the ordinary way to write a fleet-impact table (the
    # round-90 note's §2b writes "C12 used-by trim" as a joined cell instead).
    tbl = ["| id | lanes hit | effect |", "|---|---|---|",
           "| C12 | 20 | 1695 false E11 findings |",
           "| C03 | 15 | 97 rows gain E04 |",
           "| C09 | 9 | W04 set changes |",
           "| C10 | 2 | 11 rows gain E09 |",
           "| C02 | 0 | no live registry carries the shape |"]
    return note.rstrip("\n") + "\n\n" + "\n".join(tbl) + "\n", extra


def a_idkeyed_section2b(note, extra):
    # pure reformat of the note's OWN §2b table: the id moves into its own
    # cell, every other cell is byte-preserved. No content is added.
    lines = note.split("\n")
    out, i, hit = [], 0, 0
    while i < len(lines):
        if lines[i].strip() == "| survivor | lanes hit | effect on live registries |":
            out.append("| id | survivor | lanes hit | effect on live registries |")
            out.append("|---|---|---|---|")
            i += 2  # skip header + separator
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].split("|")[1:-1]]
                m = re.match(r"^(C\d\d)(?:, )?(.*)$", cells[0])
                assert m, lines[i]
                out.append("| %s | %s | %s | %s |" % (m.group(1), m.group(2) or "—",
                                                      cells[1], cells[2]))
                hit += 1
                i += 1
            continue
        out.append(lines[i])
        i += 1
    print("    section-2b rows reformatted:", hit, file=sys.stderr)
    return "\n".join(out), extra


def a_ident(note, extra):
    return note, extra


ATTEMPTS = [
    ("A0-control-honest", "unchanged note at 84904d41 (harness control)", a_ident),
    ("A1-fenced-second-table", "inverted 12-row table inside a ``` fence", a_fenced),
    ("A2-html-table", "inverted 12-row HTML table", a_html),
    ("A3-prose-verdict", "inverted verdicts as prose, no table", a_prose),
    ("A4-escaped-pipe", "honest row with a standard Markdown escaped \\| in a cell", a_escaped),
    ("A5-dup-header", "a duplicated verdict header before C02", a_dupheader),
    ("A6-drop-C12", "the C12 row removed", a_drop),
    ("A7-measured-in-fence", "an example `measured: 7/12 killed` inside a fence", a_measured_fence),
    ("A8-bold-ids", "honest table, id cells bolded (**C01**)", a_bold_ids),
    ("A9-backtick-verdicts", "honest table, verdict cells code-spanned (`KILLED`)", a_backtick_verdict),
    ("A10-coverage-decoy", "the Core README coverage row removed; the 'not admitted' row remains", a_coverage_decoy),
    ("A11-source-decoy", "S320 stays `mined`, lesson grounding reduced to S320 + URL", a_source_decoy),
    ("A12-id-keyed-impact", "honest note + a second table keyed by ids C02..C12 with no verdicts", a_idkeyed_impact),
    ("A13-id-keyed-2b-reformat", "the note's own 2b impact table reformatted so the id is its own cell", a_idkeyed_section2b),
]


def run_one(scratch, out, name, desc, fn, counter):
    d = os.path.join(scratch, "att-" + name)
    repo = os.path.join(d, "repo")
    work = os.path.join(d, "work")
    os.makedirs(d, exist_ok=True)
    subprocess.run(["git", "clone", "--shared", "-q", LANE, repo], check=True)
    git(repo, "checkout", "-q", "--detach", REV)
    top = git(repo, "rev-parse", "--show-toplevel").stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(repo), ("toplevel", top, repo)
    note = show(REV, NOTE)
    extra = {README: show(REV, README), LESSON: show(REV, LESSON)}
    note2, extra2 = fn(note, extra)
    with open(os.path.join(repo, NOTE), "w") as f:
        f.write(note2)
    for path, text in extra2.items():
        with open(os.path.join(repo, path), "w") as f:
            f.write(text)
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "--allow-empty", "-m", "T92C1 attempt " + name, identity=True)
    rev = git(repo, "rev-parse", "HEAD").stdout.strip()
    # the committed bytes must be exactly what we wrote (note + docs)
    assert git(repo, "cat-file", "blob", rev + ":" + NOTE).stdout == note2, name + ": note bytes"
    for path, text in extra2.items():
        assert git(repo, "cat-file", "blob", rev + ":" + path).stdout == text, name + ": " + path
    os.makedirs(work)
    p = subprocess.run(["python3", "-I", counter, "--repo", repo, "--rev", rev, "--work", work],
                       capture_output=True, text=True)
    body = ("# attempt %s\ndescription: %s\n# state rev %s (parent %s)\n# counter sha256 %s\n"
            "# command: python3 -I measure-v92.py --repo <clone> --rev %s --work <empty>\n"
            "# note sha256 %s\n# exit %d\n%s%s" % (
                name, desc, rev, REV, hashlib.sha256(open(counter, "rb").read()).hexdigest(),
                rev, hashlib.sha256(note2.encode()).hexdigest(), p.returncode,
                p.stdout, p.stderr))
    with open(os.path.join(out, "T92C1-%s.out" % name), "w") as f:
        f.write(body)
    with open(os.path.join(out, "T92C1-%s-note.md" % name), "w") as f:
        f.write(note2)
    summary = ""
    for line in p.stdout.split("\n"):
        if line.startswith("C1_SUMMARY") or line.startswith("C1_CONJUNCTS") or \
                line.startswith("C1_R92_PASS=") or line.startswith("C1_SETUP"):
            summary += "    " + line + "\n"
    return "%s exit=%d\n%s" % (name, p.returncode, summary)


def main():
    scratch = sys.argv[1]
    out = sys.argv[2]
    counter = os.path.join(scratch, "measure-v92.py")
    assert os.path.isdir(scratch) and os.path.isdir(out)
    h = hashlib.sha256(open(counter, "rb").read()).hexdigest()
    assert h == "be5a9221b36983d6c45e983c398ee9c9c088b374d36fb17e2ae67f50ad749ea9", h
    print("counter sha256", h, "rev", REV, flush=True)
    res = []
    with cf.ThreadPoolExecutor(max_workers=12) as ex:
        futs = [ex.submit(run_one, scratch, out, n, d, f, counter) for n, d, f in ATTEMPTS]
        for fu in cf.as_completed(futs):
            r = fu.result()
            print(r, flush=True)
            res.append(r)
    print("DONE", len(res))


if __name__ == "__main__":
    main()
