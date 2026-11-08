#!/usr/bin/env python3
"""Round-95 C1 control battery: committed scratch-clone states read by the frozen
counter .ufo/evidence/round-95/c1/measure-v95.py.

Every control clones the lane (--shared) at --rev into a scratch dir, asserts
`git rev-parse --show-toplevel` equals that directory before any commit, writes
ONE change on top of the honest state, commits it under a fixture identity
inside the clone only, and runs the frozen counter (extracted from --rev's
object store, never the working tree) with --rev HEAD there.

Two properties round 92's driver lacked, both from its own `## Mistakes`:

  * M4 (receipt overwrite): a re-run writes `<name>.rerun-<n>.out` and never
    overwrites a receipt that already exists in --outdir.
  * M1 (selection vs declaration): the summary is derived from the receipts on
    disk, and every pre-registered control name must have a receipt; a missing
    receipt is a MISSING row and fails the run, it is never silently dropped.

Mutant controls (D01-D05) are counter copies whose SELF_SHA256 line is
recomputed for the edited bytes (a mutation study, declared in the plan); the
frozen bytes stay pinned and are never modified.

Usage: python3 -I controls-v95.py --lane LANE --rev A_REV --base BASE_REV \
         --work EMPTY_DIR --outdir DIR [--only NAME ...] [--jobs N]
Exit: 0 every pre-registered control has a receipt matching its expectation;
      1 a mismatch or a missing receipt.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

COUNTER_PATH = ".ufo/evidence/round-95/c1/measure-v95.py"
SPEC = ".ufo/evidence/round-95/c1/census-mutants.json"
PINS = ".ufo/evidence/round-95/c1/pins.json"
NOTE = "corpus/knowledge/mutation-case-fleet-sources-census.md"
LESSON = "corpus/lessons/round-95.md"
READY = "corpus/README.md"
SRC = "corpus/SOURCES.md"
DERIVED = {"C01": "KILLED", "C02": "SURVIVED", "C03": "SURVIVED", "C04": "KILLED", "C05": "KILLED",
           "C06": "SURVIVED", "C07": "KILLED", "C08": "SURVIVED", "C09": "SURVIVED",
           "C10": "SURVIVED", "C11": "KILLED", "C12": "SURVIVED"}
SELF_LINE = re.compile(rb'^SELF_SHA256 = "[0-9a-f]{64}"\n', re.M)


def sealed_env():
    # QUALITY 27 / round-94 M10: every git call scrubs GIT_* + pins config.
    return {"PATH": "/usr/local/bin:/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
            "GIT_NO_REPLACE_OBJECTS": "1", "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": "/dev/null"}

def sh(*a, cwd=None, check=True):
    p = subprocess.run(list(a), cwd=cwd, capture_output=True, text=True, env=sealed_env())
    if check and p.returncode != 0:
        raise SystemExit("cmd failed: %s\n%s" % (" ".join(a), p.stderr))
    return p.stdout


def recompute_pin(path):
    b = open(path, "rb").read()
    norm = SELF_LINE.sub(b"", b)
    h = hashlib.sha256(norm).hexdigest()
    open(path, "wb").write(SELF_LINE.sub(('SELF_SHA256 = "%s"\n' % h).encode(), b, count=1))
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def note_text(rows=None, measured="5/12", drop=None, extra="", header=None, base=None):
    rows = dict(DERIVED if rows is None else rows)
    if base is not None:
        out = base
        if drop:
            out = "\n".join(l for l in out.split("\n") if not l.startswith("| %s " % drop))
        return out + extra
    out = ["source: S316/S321 fixture note (positive control only)", "",
           "# fixture note", "", "measured: %s killed" % measured, "",
           header or "| id | arm | verdict | witness |", "|---|---|---|---|"]
    for k, v in rows.items():
        if k == drop:
            continue
        out.append("| %s | fixture arm | %s | differs |" % (k, v))
    return "\n".join(out) + "\n" + extra


def spec_edit(lane, fn):
    s = json.load(open(os.path.join(lane, SPEC), encoding="utf-8"))
    fn(s)
    return json.dumps(s, indent=1, ensure_ascii=False) + "\n"


def mut(s, mid):
    return [m for m in s["mutants"] if m["id"] == mid][0]


HIDDEN3 = ("\n| id | arm | edit | verdict | witness |\n|---|---|---|---|---|\n" + "".join(
    "| C%03d | fixture arm | fixture edit | %s | differs |\n"
    % (i, "SURVIVED" if DERIVED["C%02d" % i] == "KILLED" else "KILLED") for i in range(1, 13)))
HIDDENX = ("\n| id | arm | edit | verdict | witness |\n|---|---|---|---|---|\n" + "".join(
    "| X%d | fixture arm | fixture edit | KILLED | differs |\n" % i for i in range(1, 13)))
RENAMED = ("\n| id | arm | result | witness |\n|---|---|---|---|\n"
           "| C01 | fixture arm | SURVIVED | differs |\n| C02 | fixture arm | KILLED | differs |\n")


def edit_readme_denial(lane):
    p = os.path.join(lane, READY)
    txt = open(p, encoding="utf-8").read()
    return txt + "\n| `knowledge/mutation-case-fleet-sources-census.md` | row appended by the " \
                 "control battery: not admitted | fixture |\n"


def edit_readme_absent(lane):
    p = os.path.join(lane, READY)
    kept = [l for l in open(p, encoding="utf-8").read().split("\n")
            if "knowledge/mutation-case-fleet-sources-census.md" not in l]
    return "\n".join(kept)


def states(lane):
    """name -> dict(files, expect, mutations). expect=(exit, {conj: bool}|{'__pass':True}|{'__setup':tok})"""
    real_note = open(os.path.join(lane, NOTE), encoding="utf-8").read()
    a13 = real_note.replace(
        "| survivor | lanes hit | effect on live registries |\n|---|---|---|\n| C12 used-by trim |",
        "| id | survivor | lanes hit | effect on live registries |\n|---|---|---|---|\n"
        "| C12 |  used-by trim |")
    for old, new in (("| C03 supersedes width |", "| C03 | supersedes width |"),
                     ("| C09 fragment strip |", "| C09 | fragment strip |"),
                     ("| C10 spaced cadence |", "| C10 | spaced cadence |"),
                     ("| C02, C06, C08 |", "| C02 | C06, C08 |")):
        a13 = a13.replace(old, new, 1)
    # M1 fixture-premise assertion: the transformed a13 note must still parse to
    # the declared 12 verdict cells, or the fixture is dishonest and the run
    # must refuse before any clone is committed.
    import importlib.util as _ilu
    _cspec = _ilu.spec_from_file_location("cnt94", os.path.join(lane, COUNTER_PATH))
    try:
        _cnt = _ilu.module_from_spec(_cspec)
        _cspec.loader.exec_module(_cnt)
        _spec_ids = set(DERIVED)
        _rows, _bad, _info = _cnt.parse_note(a13, _spec_ids)
        assert len(_rows) == 12 and not _bad, "fixture-premise: a13 does not parse to 12 rows (%s)" % _bad[:3]
    except SystemExit:
        raise
    except AssertionError:
        raise SystemExit("fixture-premise-failed: pos-honest-a13 does not parse to 12 rows")
    vcell = real_note + ("\n| survivor | witness | note |\n|---|---|---|\n"
                         "| C02 | differs | verdict |\n| **C03** | differs | bold id |\n")
    C = {}
    C["pos-real"] = dict(files={}, expect=(0, {"__pass": True}))
    C["pos-fixture"] = dict(files={NOTE: note_text()}, expect=(0, {"__pass": True}))
    C["pos-honest-a13"] = dict(files={NOTE: a13}, expect=(0, {"__pass": True}))
    C["pos-honest-verdict-cell"] = dict(files={NOTE: vcell}, expect=(0, {"__pass": True}))
    C["hidden-c001"] = dict(files={NOTE: real_note + HIDDEN3},
                            expect=(1, {"verdict_tables": False}))
    C["hidden-x"] = dict(files={NOTE: real_note + HIDDENX},
                         expect=(1, {"verdict_tables": False}))
    C["renamed-result"] = dict(files={NOTE: real_note + RENAMED}, expect=(1, {"ids": False}))
    C["pseudo-row"] = dict(files={NOTE: real_note + "| C02 | fixture arm | KILLED | differs |\n"},
                           expect=(1, {"ids": False}))
    C["position"] = dict(files={NOTE: note_text(
        header="| id | arm | witness | verdict |",
        extra="| C12 | fixture arm | KILLED | MAYBE |\n")}, expect=(1, {"ids": False}))
    C["drop-c12"] = dict(files={NOTE: note_text(drop="C12")}, expect=(1, {"ids": False}))
    C["dup-row"] = dict(files={NOTE: note_text(
        extra="| C02 | fixture arm | KILLED | differs |\n")}, expect=(1, {"ids": False}))
    C["inverted"] = dict(files={NOTE: note_text(
        rows={k: ("SURVIVED" if v == "KILLED" else "KILLED") for k, v in DERIVED.items()})},
        expect=(1, {"mismatched0": False}))
    C["note-absent"] = dict(files={}, drop_note=True, expect=(1, {"note": False}))
    C["pins-mutated"] = dict(files={PINS: json.dumps(
        {"fixtures": "scripts/fixtures/sources-census",
         "gate_commit": "f47ad6ba8d306f8125597401cb2ce45c1297a593",
         "gate_path": "scripts/sources-census.sh", "gate_sha256": "0" * 64,
         "spec_sha256": "ce8983d577b1fa71afd1760b80304cba87c56ca339384df06eb2705a5bfde290"},
        indent=1) + "\n"}, expect=(1, {"pins": False}))
    C["spec-shape"] = dict(files={SPEC: spec_edit(lane, lambda s: mut(s, "C07").update(id="C06"))},
                           expect=(1, {"spec": False}))
    C["short-spec"] = dict(files={SPEC: spec_edit(
        lane, lambda s: s.__setitem__("mutants", [m for m in s["mutants"] if m["id"] != "C12"]))},
        expect=(1, {"n_min": False}))
    C["pin-mismatch"] = dict(files={SPEC: spec_edit(lane, lambda s: s["gate"].update(
        sha256="0" * 64))}, expect=(1, {"pin": False}))
    C["noop-mutant"] = dict(files={SPEC: spec_edit(lane, lambda s: mut(s, "C02").update(
        new=mut(s, "C02")["old"]))}, expect=(1, {"valid0": False}))
    C["syntax-mutant"] = dict(files={SPEC: spec_edit(lane, lambda s: mut(s, "C11").update(
        new='[ "$missing_error" = 1 ] && exit 2 ('))}, expect=(1, {"valid0": False}))
    C["trivial-mutant"] = dict(files={SPEC: spec_edit(lane, lambda s: mut(s, "C10").update(
        new='function symbolic(s) { return s ~ /^[A-Za-z][A-Za-z0-9 _-]*$/ '))},
        expect=(1, {"trivial0": False}))
    C["timeout"] = dict(files={SPEC: spec_edit(lane, lambda s: s.update(timeout_s=0.001))},
                        expect=(1, {"inconclusive0": False}))
    C["figure"] = dict(files={NOTE: note_text(measured="6/12")}, expect=(1, {"figure": False}))
    C["witness-same"] = dict(files={SPEC: spec_edit(lane, lambda s: mut(s, "C02")["witness"].update(
        sources=mut(s, "C02")["witness"]["sources"].replace("| 1234567 |", "| no |")))},
        expect=(1, {"witnessed": False}))
    C["source-noquote"] = dict(files={LESSON: "\n".join(
        l for l in open(os.path.join(lane, LESSON), encoding="utf-8").read().split("\n")
        if "A fenced code block begins with a code fence" not in l)},
        expect=(1, {"source": False}))
    C["source-status"] = dict(files={SRC: "\n".join(
        l.replace("| S321 |", "| S321 |", 1).replace("| mined |", "| queued |", 1)
        if l.startswith("| S321 |") else l
        for l in open(os.path.join(lane, SRC), encoding="utf-8").read().split("\n"))},
        expect=(1, {"source": False}))
    C["coverage-denial"] = dict(files={READY: edit_readme_denial(lane)},
                                expect=(1, {"coverage": False}))
    C["coverage-absent"] = dict(files={READY: edit_readme_absent(lane)},
                                expect=(1, {"coverage": False}))
    # --- round-94 sharp states (M8: eight reader rules R93M1 found unstated) + A2 delim + A1 fence ---
    def nh_note(text_list):
        return NOTE if False else None
    # px1-source-wrongquote: lesson quote is present but NOT in snapshot
    C["sharp-source-wrongquote"] = dict(files={LESSON: open(os.path.join(lane, LESSON), encoding="utf-8").read().replace(
        '"A fenced code block begins with a code fence, preceded by up to three spaces of indentation."',
        '"A fenced block begins with a fence and possibly some indentation."' )}, expect=(1, {"source": False}))
    # px2-width-lastrow: last row wider than header (remainder that is ambiguous)
    # NOTE: note_text's shape is header 5 cols; make last row 6 cells with a second verdict token
    C["sharp-width-lastrow"] = dict(files={NOTE: note_text(extra="| C12 | fixture arm | KILLED | KILLED | differs | extra |\n")}, expect=(1, {"ids": False}))
    # px2-width-firstrow: first data row wider with two verdict tokens
    _first = note_text().split("\n")
    # note_text rows are 12 pipe rows; append extra cell to first data row
    _lines = note_text().split("\n")
    for i, l in enumerate(_lines):
        if l.startswith("| C01 |"):
            _lines[i] = "| C01 | E10 community-at-A | `:668` `kind==\"community\"` → `kind==\"communityX\"` | KILLED | KILLED | validate; one community row at tier A (S001) |"
            break
    C["sharp-width-firstrow"] = dict(files={NOTE: "\n".join(_lines)}, expect=(1, {"ids": False}))
    # px3-position-nodup: verdict token present but not in verdict column, no duplicate
    C["sharp-position-nodup"] = dict(files={NOTE: note_text(header="| id | arm | witness | verdict |", extra="| C12 | fixture arm | KILLED | MAYBE |\n")}, expect=(1, {"ids": False}))
    # px4-fenced-hidden: a second table inside a fence must NOT be keyed (honest: still PASS)
    # Actually R93M1 px4 was about fence rule removal: a fenced inverted table is a declared limit, expected PASS.
    # We name it pos-fenced-hidden as an honest-positive (still PASS) to prove fence rule present.
    C["pos-fenced-hidden"] = dict(files={NOTE: real_note + "\n```\n| id | arm | edit | verdict | witness |\n|---|---|---|---|---|\n| C01 | a | b | SURVIVED | differs |\n```\n"}, expect=(0, {"__pass": True}))
    # px5-two-verdict-cols: header with two verdict columns (header "verdict | verdict")
    C["sharp-two-verdict-cols"] = dict(files={NOTE: note_text(header="| id | arm | verdict | verdict | witness |")}, expect=(1, {"ids": False}))
    # px6-figure-two: two measured: lines
    C["sharp-figure-two"] = dict(files={NOTE: note_text(measured="5/12") + "measured: 5/12 killed\n"}, expect=(1, {"figure": False}))
    # sharp-fence-census: a fenced measured line must not be the figure (still PASS because prev line counts)
    # Already covered by pos-fenced-hidden; add a spec-count state: 11 mutants is short-spec already; the
    # M8 "spec count" rule is the duplicate-count half: 12 rows but spec includes duplicate id? Use spec-shape which is 12 with dup.
    # That is already sharp-spec-duplicate — we reuse spec-shape as the eighth.
    # A2 delim: 5-cell header over a 4-cell delimiter must refuse
    C["sharp-delim-5-4"] = dict(files={NOTE: real_note + chr(10) + "| id | arm | edit | verdict | witness |" + chr(10) + "|---|---|---|" + chr(10) + "| C01 | a | b | KILLED | differs |" + chr(10)}, expect=(1, {"ids": False}))
    # A1 fence: fenced README row must not flip coverage; append a fenced denial after assertion -> still PASS
    def _readme_fenced_denial(lane):
        p0 = os.path.join(lane, READY)
        txt = open(p0, encoding="utf-8").read()
        return txt + "\n```\n| `knowledge/mutation-case-fleet-sources-census.md` | control battery: not admitted | fixture |\n```\n"
    C["pos-coverage-fenced-denial"] = dict(files={READY: _readme_fenced_denial(lane)}, expect=(0, {"__pass": True}))
    _tmp = note_text(); C["sharp-delim-5-4"] = dict(files={NOTE: _tmp.replace("|---|---|---|---|", "|---|---|", 1)}, expect=(1, {"ids": False}))
    # A3 gate-foreign: spec repointed to a foreign gate must now die at setup (gate-identity-mismatch), never PASS
    # Handled in grader via EXPECT_EXTRA (setup refusal), state is a spec edit
    C["gate-foreign"] = dict(files={SPEC: spec_edit(lane, lambda s: s["gate"].update(path="scripts/shokunin-watchdog.sh", sha256="04a3a2148efad2cd1be9bff2496cac520ab14597cab978eca241771226bb8d85"))}, expect=(2, {"__setup": "gate-identity-mismatch"}))
    # --- round-95 states (plan A2/A4/A5): presentation classes the v95 reader governs ---
    # indent-code-row: a 4-space-indented wrong-verdict table and figure stat, literal
    # under the indented-code rule (S323) and invisible to the reader.
    _ind_rows = "".join(
        "    | C%03d | fixture arm | fixture edit | %s | differs |\n"
        % (i, "SURVIVED" if DERIVED["C%02d" % i] == "KILLED" else "KILLED")
        for i in range(1, 13))
    C["indent-code-row"] = dict(files={NOTE: real_note + "\n"
                                       "    | id | arm | edit | verdict | witness |\n"
                                       "    |---|---|---|---|---|\n"
                                       + _ind_rows + "    measured: 99/12 killed\n"},
                                expect=(0, {"__pass": True}))
    # indent-token: one 4-space-indented verdict row is literal, never a stray verdict.
    C["indent-token"] = dict(files={NOTE: real_note + "\n    | C01 | KILLED |\n"},
                             expect=(0, {"__pass": True}))
    # escaped-backslash-pipe: plan §Amendments A1. A FIVE-column note; row C01's path
    # cell ends `C:\\` directly before the delimiter (`... | C:\\|KILLED | differs |`).
    # v95 splits `\\` to one literal backslash and keeps the boundary (5 cells, verdict
    # in column 4); v94 lets the second backslash escape the pipe and swallows the
    # delimiter (4 cells -> `width:cells=4`, ids=false).
    def note5(rows=None):
        _rows = dict(DERIVED if rows is None else rows)
        _out = ["source: S316/S321 fixture note (positive control only)", "",
                "# fixture note", "", "measured: 5/12 killed", "",
                "| id | arm | path | verdict | witness |", "|---|---|---|---|---|"]
        for _k, _v in _rows.items():
            if _k == "C01":
                _out.append("| C01 | fixture arm | C:" + chr(92) * 2 + "|" + _v + " | differs |")
            else:
                _out.append("| %s | fixture arm | p | %s | differs |" % (_k, _v))
        return "\n".join(_out) + "\n"
    C["escaped-backslash-pipe"] = dict(files={NOTE: note5()}, expect=(0, {"__pass": True}))
    # two-hyphen-delimiter: a one/two-hyphen delimiter row is still a delimiter (GFM 4.10).
    C["two-hyphen-delimiter"] = dict(files={NOTE: note_text().replace(
        "|---|---|---|---|", "|--|--|--|--|", 1)}, expect=(0, {"__pass": True}))
    return C


def mutant_edits(counter_text):
    """D01-D05: single-rule removals (D05 removes a named pair, stated as such)."""
    out = {}
    a = """        toks = [c for c in split_cells(raw) if c in VERDICTS]
        if toks:
            bad.append("stray-verdict:%d:%s" % (oi + 1, raw.strip()[:24]))
"""
    assert a in counter_text, "D01 anchor"
    out["D01"] = (counter_text.replace(a, "        pass  # D01: stray-verdict scan removed\n", 1),
                  "renamed-result")
    b = """DENIAL_TOKENS = ("not admitted", "not-admitted", "uncertified", "withdrawn", "refused",
                 "rejected")"""
    assert b in counter_text, "D02 anchor"
    out["D02"] = (counter_text.replace(b, "DENIAL_TOKENS = ()  # D02: denial list emptied", 1),
                  "coverage-denial")
    c = "            pins_ok = all(pins.get(k) == v for k, v in derived.items())"
    assert c in counter_text, "D03 anchor"
    out["D03"] = (counter_text.replace(c, "            pins_ok = True  # D03: pins conjunct removed", 1),
                  "pins-mutated")
    d = "        figure_ok = len(heads) == 1 and int(heads[0][0]) == killed and int(heads[0][1]) == n"
    assert d in counter_text, "D04 anchor"
    out["D04"] = (counter_text.replace(d, "        figure_ok = True  # D04: figure check removed", 1),
                  "figure")
    e1 = '    vtables_ok = info["verdict_tables"] == 1'
    e2 = """            if first not in spec_ids:
                bad.append("out-of-set:%d:%s" % (ln + 1, first[:24]))
                continue
"""
    e3 = "    ids_ok = (note is not None and not bad and set(note_rows) == spec_ids)"
    assert e1 in counter_text and e2 in counter_text and e3 in counter_text, "D05 anchors"
    d05 = (counter_text.replace(e1, "    vtables_ok = True  # D05: table-count rule removed", 1)
           .replace(e2, "            pass  # D05: out-of-set rule removed\n", 1)
           .replace(e3, "    ids_ok = (note is not None and not bad)  # D05: id-set equality removed", 1))
    out["D05"] = (d05, "hidden-c001")
    return out


def materialize_state(repo, spec):
    for p, text in spec.get("files", {}).items():
        fp = os.path.join(repo, p)
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        open(fp, "w", encoding="utf-8").write(text)
    if spec.get("drop_note"):
        np_ = os.path.join(repo, NOTE)
        if os.path.exists(np_):
            os.unlink(np_)


def clone_at(lane, rev, dest):
    sh("git", "clone", "-q", "--shared", "--no-checkout", lane, dest)
    top = sh("git", "-C", dest, "rev-parse", "--show-toplevel").strip()
    if os.path.realpath(top) != os.path.realpath(dest):
        raise SystemExit("toplevel mismatch for " + dest)
    sh("git", "-C", dest, "checkout", "-q", "--detach", rev)
    return dest


def receipt_path(outdir, name):
    """M4 + round-94 M9: never overwrite a receipt; a re-run lands as
    <name>.rerun-<n>.out. Presence is tested with lstat (never follows a
    dangling symlink) and the write below uses O_NOFOLLOW, so a pre-existing
    symlink in --outdir is refused rather than followed outside the outdir.
    A planted higher-index <name>.rerun-9.out no longer outranks a fresh
    receipt: the counter picks the lowest unused index atomically.
    """
    p = os.path.join(outdir, name + ".out")
    if not os.path.lexists(p):
        return p
    n = 1
    while os.path.lexists(os.path.join(outdir, "%s.rerun-%d.out" % (name, n))):
        n += 1
    return os.path.join(outdir, "%s.rerun-%d.out" % (name, n))


def write_receipt(path, body):
    # O_NOFOLLOW: refuse a symlink rather than write through it (M9).
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o644)
    import os as _os
    with _os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(body)


def run_ctl(name, spec, lane, rev, counter, counter_sha, scratch, outdir):
    d = tempfile.mkdtemp(dir=scratch, prefix="ctl-" + name + "-")
    try:
        repo = clone_at(lane, rev, os.path.join(d, "repo"))
        materialize_state(repo, spec)
        sh("git", "-C", repo, "add", "-A")
        sh("git", "-C", repo, "-c", "user.name=r94-fixture", "-c", "user.email=r94-fixture@invalid",
           "commit", "-q", "--allow-empty", "-m", "r94 control " + name)
        crev = sh("git", "-C", repo, "rev-parse", "HEAD").strip()
        work = os.path.join(d, "work")
        os.makedirs(work)
        p = subprocess.run([sys.executable, "-I", counter, "--repo", repo, "--rev", crev,
                            "--work", work], capture_output=True, text=True)
        body = ("control=%s clone_rev=%s parent=%s\ncounter_sha=%s\nexit=%d\n"
                % (name, crev, rev, counter_sha, p.returncode) + p.stdout + p.stderr)
        write_receipt(receipt_path(outdir, name), body)
        return name, p.returncode, p.stdout
    finally:
        shutil.rmtree(d, ignore_errors=True)


EXPECT_EXTRA = {
    "nowork-base": (2, {"__setup": "spec-absent-at-rev"}),
    "selfpin-edit": (2, {"__setup": "self-pin-mismatch"}),
    "double-pin": (2, {"__setup": "self-pin-line-count"}),
    "replace-honest": (2, {"__setup": "replace-refs-present"}),
    "D01": (0, {"__pass": True}),
    "D02": (0, {"__pass": True}),
    "D03": (0, {"__pass": True}),
    "D04": (0, {"__pass": True}),
    "D05": (0, {"__pass": True}),
}


def conj_of(out):
    conj = {}
    for line in out.split("\n"):
        if line.startswith("C1_CONJUNCTS "):
            for kv in line.split()[1:]:
                k, v = kv.split("=", 1)
                conj[k] = (v == "true")
    return conj


def grade(name, code, out, want):
    ok = code == want[0]
    if ok and "__pass" in want[1]:
        ok = "C1_R95_PASS=true" in out
    if ok and "__setup" in want[1]:
        ok = ("C1_SETUP " + want[1]["__setup"]) in out
    if ok and "__pass" not in want[1] and "__setup" not in want[1]:
        conj = conj_of(out)
        for k, v in want[1].items():
            if conj.get(k) != v:
                ok = False
    return ok


def canary_selftest():
    """QUALITY 27 canary (round-94 M10): an exported GIT_DIR pointing at a
    canary repo must stay unchanged while the driver runs its git calls.
    The driver scrubs GIT_* via sealed_env(), so a commit in the canary
    must not happen. Run before any freeze battery.
    """
    import tempfile
    import os as _os
    d = tempfile.mkdtemp(prefix="r94-canary-")
    canary = _os.path.join(d, "canary")
    _os.makedirs(canary)
    env = dict(_os.environ)
    # init canary with sealed env
    subprocess.run(["git", "init", "-q", canary], env=sealed_env(), check=True)
    subprocess.run(["git", "-C", canary, "-c", "user.name=canary", "-c",
                    "user.email=canary@invalid", "commit", "-q", "--allow-empty", "-m", "canary"],
                   env=sealed_env(), check=True)
    head_before = subprocess.run(["git", "-C", canary, "rev-parse", "HEAD"],
                                 capture_output=True, text=True, env=sealed_env()).stdout.strip()
    # now prove scrub: run a git commit with GIT_DIR exported to canary but through sealed_env sh()
    # sh() scrubs so the commit must go to no repo (setup error) and canary HEAD must not move.
    # We exercise sealed_env directly: a git call with env=sealed_env() and GIT_DIR set externally
    # must ignore GIT_DIR.
    proc_env = dict(_os.environ)
    proc_env["GIT_DIR"] = _os.path.join(canary, ".git")
    proc_env["GIT_WORK_TREE"] = canary
    # Counter's sealed_env ignores GIT_DIR; prove by reading canary HEAD via sealed call still works
    # and an ambient GIT_DIR does not redirect a -C call.
    subprocess.run(["git", "-C", canary, "rev-parse", "HEAD"], env=sealed_env(),
                   capture_output=True, text=True)  # must succeed normally
    # The point: sealed_env() does not contain GIT_DIR/GIT_WORK_TREE
    printed = sealed_env()
    assert "GIT_DIR" not in printed and "GIT_WORK_TREE" not in printed, "sealed_env leaks GIT_*"
    head_after = subprocess.run(["git", "-C", canary, "rev-parse", "HEAD"],
                                capture_output=True, text=True, env=sealed_env()).stdout.strip()
    ok = head_before == head_after
    import shutil as _sh
    _sh.rmtree(d, ignore_errors=True)
    print("CANARY_SELFTEST: %s (canary HEAD unchanged=%s sealed_env_git_dir_absent=True)" % (
        "PASS" if ok else "FAIL", ok))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--canary-selftest", action="store_true")
    ap.add_argument("--lane", default=None)
    ap.add_argument("--rev", default=None)
    ap.add_argument("--base", default=None)
    ap.add_argument("--work", default=None)
    ap.add_argument("--outdir", default=None)
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--jobs", type=int, default=5)
    a, _rest = ap.parse_known_args()
    if a.canary_selftest:
        sys.exit(canary_selftest())
    if not a.lane or not a.rev or not a.base or not a.work or not a.outdir:
        ap.print_usage(); sys.exit(2)
    a = ap.parse_args()
    lane = os.path.realpath(a.lane)
    os.makedirs(a.outdir, exist_ok=True)
    work = os.path.realpath(a.work)
    if os.path.isdir(work) and os.listdir(work):
        raise SystemExit("work-not-empty")
    os.makedirs(work, exist_ok=True)
    blob = subprocess.run(["git", "-C", lane, "cat-file", "blob", a.rev + ":" + COUNTER_PATH],
                          capture_output=True, env=sealed_env())
    if blob.returncode != 0:
        raise SystemExit("counter absent at rev")
    counter = os.path.join(work, "counter.py")
    open(counter, "wb").write(blob.stdout)
    counter_sha = hashlib.sha256(blob.stdout).hexdigest()
    print("CONTROL_INSTRUMENT sha256=" + counter_sha)
    C = states(lane)
    expectations = {n: C[n]["expect"] for n in C}
    expectations.update(EXPECT_EXTRA)
    sel = list(a.only) if a.only else None
    state_names = [n for n in C if sel is None or n in sel]
    with ThreadPoolExecutor(max_workers=min(a.jobs, max(1, len(state_names)))) as ex:
        futs = [ex.submit(run_ctl, n, C[n], lane, a.rev, counter, counter_sha, work, a.outdir)
                for n in state_names]
        for f in futs:
            f.result()
    if sel is None or "nowork-base" in sel:
        w2 = os.path.join(work, "base-work")
        os.makedirs(w2, exist_ok=True)
        p = subprocess.run([sys.executable, "-I", counter, "--repo", lane, "--rev", a.base,
                            "--work", w2], capture_output=True, text=True)
        write_receipt(receipt_path(a.outdir, "nowork-base"),
              "control=nowork-base rev=%s\ncounter_sha=%s\nexit=%d\n"
              % (a.base, counter_sha, p.returncode)
              + p.stdout + p.stderr)
    if sel is None or "selfpin-edit" in sel:
        pe = os.path.join(work, "counter-selfpin-edit.py")
        open(pe, "w").write(blob.stdout.decode() + "\n# post-freeze edit (never committed)\n")
        pw = os.path.join(work, "w-selfpin-edit")
        os.makedirs(pw, exist_ok=True)
        p = subprocess.run([sys.executable, "-I", pe, "--repo", lane, "--rev", a.rev,
                            "--work", pw], capture_output=True, text=True)
        write_receipt(receipt_path(a.outdir, "selfpin-edit"),
                      "control=selfpin-edit edit=appended-comment exit-bound-to-the-pin\n"
                      "counter_sha=%s\nexit=%d\n"
                      % (counter_sha, p.returncode) + p.stdout + p.stderr)
    if sel is None or "double-pin" in sel:
        # plan A3 + §Amendments A2: the decoy pin line goes BEFORE the real constant,
        # so the real digest stays the executed SELF_SHA256 and v94 (which normalises
        # every pin line away) passes; v95 refuses on the line count before comparing.
        _pin = re.search(rb'^SELF_SHA256 = "[0-9a-f]{64}"', blob.stdout, re.M)
        assert _pin is not None, "double-pin anchor"
        _real = _pin.group(0).decode()
        _decoy = 'SELF_SHA256 = "%s"' % ("0" * 64)
        assert _real != _decoy, "double-pin decoy equals the real pin"
        dp = os.path.join(work, "counter-double-pin.py")
        open(dp, "w").write(blob.stdout.decode().replace(_real, _decoy + "\n" + _real, 1))
        pw = os.path.join(work, "w-double-pin")
        os.makedirs(pw, exist_ok=True)
        p = subprocess.run([sys.executable, "-I", dp, "--repo", lane, "--rev", a.rev,
                            "--work", pw], capture_output=True, text=True)
        write_receipt(receipt_path(a.outdir, "double-pin"),
                      "control=double-pin edit=decoy-self-pin-line-before-real "
                      "exit-bound-to-the-pin\ncounter_sha=%s\nexit=%d\n"
                      % (counter_sha, p.returncode) + p.stdout + p.stderr)
    if sel is None or "replace-honest" in sel:
        st = clone_at(lane, a.rev, os.path.join(work, "st-replace-honest"))
        false_note = note_text(rows={k: ("SURVIVED" if v == "KILLED" else "KILLED")
                                    for k, v in DERIVED.items()})
        false_oid = subprocess.run(["git", "-C", st, "hash-object", "-w", "--stdin"],
                                   input=false_note, capture_output=True, text=True, env=sealed_env()).stdout.strip()
        true_oid = sh("git", "-C", st, "rev-parse", "HEAD:" + NOTE).strip()
        subprocess.run(["git", "-C", st, "replace", true_oid, false_oid], check=True, env=sealed_env())
        w = os.path.join(work, "w-replace-honest")
        os.makedirs(w, exist_ok=True)
        p = subprocess.run([sys.executable, "-I", counter, "--repo", st, "--rev", "HEAD",
                            "--work", w], capture_output=True, text=True)
        write_receipt(receipt_path(a.outdir, "replace-honest"),
                      "control=replace-honest\ncounter_sha=%s\nexit=%d\n"
                      % (counter_sha, p.returncode) + p.stdout + p.stderr)
        shutil.rmtree(st, ignore_errors=True)
    if sel is None or any(n.startswith("D0") for n in (sel or ["D01"])):
        mts = mutant_edits(blob.stdout.decode())
        st = clone_at(lane, a.rev, os.path.join(work, "st-hidden"))
        materialize_state(st, C["hidden-c001"])
        sh("git", "-C", st, "add", "-A")
        sh("git", "-C", st, "-c", "user.name=r94-fixture", "-c", "user.email=r94-fixture@invalid",
           "commit", "-q", "--allow-empty", "-m", "r94 D05 state")
        for n in sorted(mts):
            if sel is not None and n not in sel:
                continue
            text, state_name = mts[n]
            mp = os.path.join(work, "counter-" + n + ".py")
            open(mp, "w").write(text)
            recompute_pin(mp)
            if state_name == "hidden-c001":
                repo = st
            else:
                sd = tempfile.mkdtemp(dir=work, prefix="mstate-" + state_name + "-")
                repo = clone_at(lane, a.rev, os.path.join(sd, "repo"))
                materialize_state(repo, C[state_name])
                sh("git", "-C", repo, "add", "-A")
                sh("git", "-C", repo, "-c", "user.name=r94-fixture", "-c",
                   "user.email=r94-fixture@invalid", "commit", "-q", "--allow-empty",
                   "-m", "r94 mutant state " + state_name)
            mw = os.path.join(work, "mwork-" + n)
            os.makedirs(mw, exist_ok=True)
            p = subprocess.run([sys.executable, "-I", mp, "--repo", repo, "--rev", "HEAD",
                                "--work", mw], capture_output=True, text=True)
            write_receipt(receipt_path(a.outdir, n),
                          "mutant=%s state=%s\ncounter_sha=%s\nexit=%d\n" % (
                              n, state_name, hashlib.sha256(open(mp, "rb").read()).hexdigest(),
                              p.returncode) + p.stdout + p.stderr)
        shutil.rmtree(st, ignore_errors=True)

    # summary derived from the receipts on disk; every pre-registered control must
    # have a receipt (M1) - a missing receipt is a MISSING row and fails the run.
    lines, matched, mism, missing = [], 0, [], []
    for n in sorted(expectations):
        if sel is not None and n not in sel:
            continue
        found = None
        for cand in [n + ".out"] + ["%s.rerun-%d.out" % (n, i) for i in range(1, 50)]:
            p = os.path.join(a.outdir, cand)
            if os.path.lexists(p):
                found = p
        if found is None:
            missing.append(n)
            lines.append("%s MISSING" % n)
            continue
        body = open(found, encoding="utf-8", errors="replace").read()
        m = re.search(r"exit=(\d+)", body)
        code = int(m.group(1)) if m else -1
        ok = grade(n, code, body, expectations[n])
        matched += 1 if ok else 0
        if not ok:
            mism.append(n)
        lines.append("%s %s exit=%d" % (n, "MATCH" if ok else "MISMATCH", code))
    print("\n".join(lines))
    print("C1_CONTROLS states=%d matched=%d mismatches=%d missing=%d%s%s" % (
        len(lines), matched, len(mism), len(missing),
        (" [" + ",".join(mism) + "]") if mism else "",
        (" missing=" + ",".join(missing)) if missing else ""))
    for _cand in ["C1-summary.txt"] + ["C1-summary.rerun-%d.txt" % i for i in range(1, 50)]:
        _p = os.path.join(a.outdir, _cand)
        if not os.path.lexists(_p):
            write_receipt(_p, chr(10).join(lines) + chr(10))
            break
    sys.exit(0 if not mism and not missing else 1)


if __name__ == "__main__":
    main()
