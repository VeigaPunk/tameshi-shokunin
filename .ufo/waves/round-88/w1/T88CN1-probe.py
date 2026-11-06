#!/usr/bin/env python3
"""T88CN1 probe — leg 11 (py-kake-ledger-guard) survivor classes and their kake-owned fixes.

Read-only on every lane: the pinned kake blob is materialized with `git show`, the five
survivor mutants are re-derived from the pre-registered spec, and every fixture lives under
--work (a scratch dir). Nothing outside --work and stdout is written.

What it measures
  1. The pre-registered spec's ten @old strings occur exactly once in the pinned blob, the
     pristine sha256 equals the ledger pin, and each re-derived mutant sha256 equals the
     sweep-results.tsv / runner table's recorded value (same mutants the ledger counted).
  2. For each of the five SURVIVED defects: the guard function the defect edits, run on the
     fixture input the kake selftest never builds, pristine vs mutant. A divergence proves
     non-equivalence; no divergence would mean the survivor is equivalent.
  3. The proposed kake-owned selftest check per survivor, evaluated against the pristine and
     the mutant reading. KILLED means the proposed check fails on the mutant and passes on
     pristine; a fix that does not kill is reported as such (no widening).

Fixtures
  F0  single ledger, pure append                     (the selftest's "append" fixture)
  F1  two governed ledgers: round-58 edited, round-59 appended   (missing: population > 1)
  F2  tree with zero governed ledgers                (missing: empty population)
  F3  single ledger, in-place edit at the last compared byte (space before the final `]`)
                                                     (missing: the truncation edge)
  F4  single ledger, in-place edit at the em dash    (the selftest's "non-prefix" fixture)

Usage: python3 -I T88CN1-probe.py --work <empty scratch dir> [--repo <kake repo>] [--rev <rev>]
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path

PIN_SHA256 = "0c12838e3d4ea441eb750fd4c6af2398cfa704e5077f6c58b053d535f8514067"
PIN_REV = "e8d3a924249983972e5163d160cf236487986c55"
PIN_PATH = "scripts/ledger_append_guard.py"
SPEC = Path("/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-88/"
            "c1/py-kake-ledger-guard.defects.spec")
# sweep-results.tsv (the counted run's own mutant hashes)
RECORDED = {
    "K_CUT_WHOLE": "95f33d55c26cba669fafd199df50a8dbf81c6c94081a2cdf57acb9e04bc0480f",
    "K_STARTSWITH": "d2bdeab6408d516ecf7efc34d1ab7b88d37230b257301110e0b02c45510fc2e5",
    "K_FILES_EQ": "adae03b8d1e0c8ade8194e7af4b424d7c7b54562b5106b06202173de28a011a3",
    "K_GLOB": "4fcc81e256338ba1b569cdc7c2e5a04f830db8e2148f41742eddf39884d8072e",
    "K_SHOW_RC": "1889925534c6dbd812518c7383eda438721cce62d1a6e538396f1cbc6ed919a3",
    "S_HEAD_SHORT": "58bb6e10bef18b2bdafa0b046a9938bbce7d74361f200849f5ad7c84e12c8e82",
    "S_OFFSET_EQ": "9dd8f80843eb953df21992a04f5674c1948168abf4c5ea62de44da950e0d7fbe",
    "S_OK_ALL": "ac7937203d5926ec62dfc8e368b25cbe4a392662a70ca36120ade01ad01374ae",
    "S_VACUOUS": "a76ea21038eea14391f68588845fc97db8c62d5b422cb8867b96b4856c5d5542",
    "S_RED_FILES": "61b403b8b20dbbabf39f90e9054c26a147afa8625ea16019bbee044242ac1bda",
}


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def parse_spec(text: str) -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    cur: dict[str, str] | None = None
    for line in text.splitlines():
        m = re.match(r"^@defect\s+(\S+)\s+\|\s*(.*)$", line)
        if m:
            cur = {"desc": m.group(2)}
            rows[m.group(1)] = cur
            continue
        m = re.match(r"^@(old|new)\s+(.*)$", line)
        if m and cur is not None:
            cur[m.group(1)] = m.group(2)
            continue
        if line.startswith("#") or not line.strip():
            cur = None if not line.strip() else cur
    for k, v in rows.items():
        if not {"old", "new"} <= set(v):
            raise SystemExit(f"spec row {k} lacks @old/@new: {v}")
    return rows


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


def git(d: Path, *args: str, env: dict[str, str] | None = None) -> str:
    out = subprocess.run(["git", "-C", str(d), *args], capture_output=True, text=True,
                         env=env, check=True)
    return out.stdout.strip()


def make_repo(d: Path) -> str:
    d.mkdir(parents=True, exist_ok=True)
    env = {**os.environ, "GIT_AUTHOR_NAME": "ctl", "GIT_AUTHOR_EMAIL": "ctl@fixture.invalid",
           "GIT_COMMITTER_NAME": "ctl", "GIT_COMMITTER_EMAIL": "ctl@fixture.invalid"}
    git(d, "init", "-q", env=env)
    top = git(d, "rev-parse", "--show-toplevel")
    if Path(top).resolve() != d.resolve():
        raise SystemExit(f"fixture toplevel {top} != {d}")
    return env  # type: ignore[return-value]


def base_text(round_dir: str = "round-58") -> str:
    return ('{\n "schema": "receipt-rewrites/v2",\n "events": [\n'
            f'  {{\n   "path": ".ufo/waves/{round_dir}/controls/a.txt",\n'
            '   "note": "prior entry \u2014 with an em dash"\n  }\n ]\n}\n')


def append_text(text: str, round_dir: str = "round-58") -> str:
    cut = text.rindex("]")
    return (text[:cut]
            + f',\n  {{\n   "path": ".ufo/waves/{round_dir}/controls/b.txt"\n  }}\n '
            + text[cut:])


def write_ledger(root: Path, round_dir: str, body: str) -> Path:
    p = root / ".ufo" / "waves" / round_dir / "receipt-rewrites.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


def commit(d: Path, env: dict[str, str], msg: str) -> str:
    git(d, "add", "-A", env=env)
    git(d, "-c", "user.name=ctl", "-c", "user.email=ctl@fixture.invalid",
        "commit", "-q", "-m", msg, env=env)
    return git(d, "rev-parse", "HEAD")


def reading(mod, root: Path, rev: str) -> dict:
    res = mod.check_tree(root, rev)
    row = res["detail"][0] if res["detail"] else {}
    return {"files": res["files"], "prefix_preserved": res["prefix_preserved"],
            "first_divergence": row.get("first_divergence"),
            "row_prefix": row.get("prefix_preserved")}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--repo", default="/home/vgpnk/Projects/shokunin/kake-shokunin")
    ap.add_argument("--rev", default=PIN_REV)
    a = ap.parse_args()
    work = Path(a.work)
    work.mkdir(parents=True, exist_ok=True)
    repo = Path(a.repo)

    blob = subprocess.run(["git", "-C", str(repo), "show", f"{a.rev}:{PIN_PATH}"],
                          capture_output=True, check=True).stdout
    pristine_path = work / "target.ledger_append_guard.py"
    pristine_path.write_bytes(blob)
    print(f"PIN rev={a.rev} path={PIN_PATH} sha256={sha(blob)} bytes={len(blob)}")
    assert sha(blob) == PIN_SHA256, "pinned blob sha256 mismatch"

    spec_rows = parse_spec(SPEC.read_text(encoding="utf-8"))
    print(f"SPEC {SPEC} defects={len(spec_rows)} sha256={sha(SPEC.read_bytes())}")

    text = blob.decode("utf-8")
    mutants: dict[str, Path] = {}
    for did, row in spec_rows.items():
        n = text.count(row["old"])
        assert n == 1, f"{did}: @old occurs {n} times"
        mpath = work / f"mutant-{did}.py"
        mpath.write_text(text.replace(row["old"], row["new"]), encoding="utf-8")
        got = sha(mpath.read_bytes())
        assert got == RECORDED[did], f"{did}: mutant sha256 {got} != recorded {RECORDED[did]}"
        mutants[did] = mpath
    print(f"MUTANTS re-derived and hash-pinned: {len(mutants)}/{len(mutants)} "
          f"(all equal sweep-results.tsv)")

    # ---- pristine selftest control (same fixture text the guard builds) -------------
    st = work / "selftest-tree"
    st.mkdir(exist_ok=True)
    env2 = make_repo(st)
    write_ledger(st, "round-58", base_text())
    rev_st = commit(st, env2, "base")
    write_ledger(st, "round-58", append_text(base_text()))
    pm = load_module(pristine_path, "pristine")
    ctl = reading(pm, st, rev_st)
    print(f"CONTROL append F0: prefix_preserved={ctl['prefix_preserved']} files={ctl['files']}")

    # ---- fixtures ----------------------------------------------------------------
    # F1: two ledgers, round-58 edited, round-59 appended
    f1 = work / "F1-two-ledgers"
    e1 = make_repo(f1)
    write_ledger(f1, "round-58", base_text("round-58"))
    write_ledger(f1, "round-59", base_text("round-59"))
    rev1 = commit(f1, e1, "base")
    write_ledger(f1, "round-58",
                 append_text(base_text("round-58"), "round-58")
                 .replace("\u2014 with an em dash", "\\u2014 with an em dash"))
    write_ledger(f1, "round-59", append_text(base_text("round-59"), "round-59"))

    # F1b: same pair as F1 but the edited ledger sorts LAST (naive 2-ledger fixture)
    f1b = work / "F1b-two-ledgers-reversed"
    e1b = make_repo(f1b)
    write_ledger(f1b, "round-58", base_text("round-58"))
    write_ledger(f1b, "round-59", base_text("round-59"))
    rev1b = commit(f1b, e1b, "base")
    write_ledger(f1b, "round-58", append_text(base_text("round-58"), "round-58"))
    write_ledger(f1b, "round-59",
                 append_text(base_text("round-59"), "round-59")
                 .replace("\u2014 with an em dash", "\\u2014 with an em dash"))

    # F2: zero governed ledgers
    f2 = work / "F2-empty-tree"
    e2 = make_repo(f2)
    (f2 / "README.txt").write_text("no ledgers here\n", encoding="utf-8")
    rev2 = commit(f2, e2, "base")

    # F3: in-place edit at the last compared byte (space before the final `]`)
    f3 = work / "F3-truncation-edge"
    e3 = make_repo(f3)
    b3 = base_text()
    write_ledger(f3, "round-58", b3)
    rev3 = commit(f3, e3, "base")
    cut3 = b3.rindex("]")                    # character index, for the string edit
    cut_b = b3.encode("utf-8").rindex(b"]")   # byte index, the guard's own cut
    edge_byte = b3[cut3 - 1]
    edited_edge = b3[:cut3 - 1] + ("\t" if edge_byte != "\t" else " ") + b3[cut3:]
    write_ledger(f3, "round-58", edited_edge)

    # F4: in-place edit at the em dash (the selftest's own non-prefix fixture)
    f4 = work / "F4-emdash"
    e4 = make_repo(f4)
    b4 = base_text()
    write_ledger(f4, "round-58", b4)
    rev4 = commit(f4, e4, "base")
    write_ledger(f4, "round-58",
                 append_text(b4).replace("\u2014 with an em dash", "\\u2014 with an em dash"))

    emdash_off = b3.encode("utf-8").index("\u2014".encode("utf-8"))
    print(f"FIXTURES F1={f1.name} F2={f2.name} F3={f3.name} (byte cut={cut_b}, edge byte "
          f"{edge_byte!r} -> '\\t') F4={f4.name} (em-dash byte offset={emdash_off})")

    fixtures = {"F1": (f1, rev1), "F1b": (f1b, rev1b), "F2": (f2, rev2), "F3": (f3, rev3),
                "F4": (f4, rev4)}
    mods = {"pristine": pm}
    for did, p in mutants.items():
        mods[did] = load_module(p, f"mut_{did}")

    print("\nREADINGS  (pristine vs each survivor mutant; the fixture the selftest never builds)")
    table = {}
    for fx, (root, rev) in fixtures.items():
        for name in ["pristine", "S_HEAD_SHORT", "S_OFFSET_EQ", "S_OK_ALL", "S_VACUOUS"]:
            r = reading(mods[name], root, rev)
            table[(fx, name)] = r
        print(f"  {fx}: pristine files={table[(fx,'pristine')]['files']} "
              f"pp={table[(fx,'pristine')]['prefix_preserved']} "
              f"off={table[(fx,'pristine')]['first_divergence']} | "
              f"S_HEAD_SHORT pp={table[(fx,'S_HEAD_SHORT')]['prefix_preserved']} "
              f"off={table[(fx,'S_HEAD_SHORT')]['first_divergence']} | "
              f"S_OFFSET_EQ off={table[(fx,'S_OFFSET_EQ')]['first_divergence']} | "
              f"S_OK_ALL pp={table[(fx,'S_OK_ALL')]['prefix_preserved']} | "
              f"S_VACUOUS pp={table[(fx,'S_VACUOUS')]['prefix_preserved']}")

    # ---- proposed kake-owned checks ---------------------------------------------
    def red_expr(drop_files: bool):
        return (lambda res: res["prefix_preserved"] is False) if drop_files else \
               (lambda res: res["prefix_preserved"] is False and res["files"] == 1)

    checks = []

    def add(sid, check_text, pristine_ok, mutant_ok, fixture):
        verdict = "KILLED" if (pristine_ok and not mutant_ok) else (
            "NOT-KILLED" if pristine_ok and mutant_ok else "PRIS-FAIL")
        checks.append({"survivor": sid, "fixture": fixture, "check": check_text,
                       "pristine": "pass" if pristine_ok else "fail",
                       "mutant": "pass" if mutant_ok else "fail", "verdict": verdict})

    # S_HEAD_SHORT: assert the truncation edge is caught and its offset named
    p3, m3 = table[("F3", "pristine")], table[("F3", "S_HEAD_SHORT")]
    add("S_HEAD_SHORT",
        "F3 non-prefix check fires and first_divergence == cut-1 (byte offset)",
        p3["prefix_preserved"] is False and p3["first_divergence"] == cut_b - 1,
        m3["prefix_preserved"] is False and m3["first_divergence"] == cut_b - 1, "F3")

    # S_OFFSET_EQ: assert the reported offset on the existing non-prefix fixture
    p4, m4 = table[("F4", "pristine")], table[("F4", "S_OFFSET_EQ")]
    add("S_OFFSET_EQ",
        "F4 non-prefix check asserts first_divergence == the em-dash byte offset",
        p4["prefix_preserved"] is False and p4["first_divergence"] == emdash_off,
        m4["prefix_preserved"] is False and m4["first_divergence"] == emdash_off, "F4")

    # S_OK_ALL: two ledgers, first diverges, second preserved
    p1, m1 = table[("F1", "pristine")], table[("F1", "S_OK_ALL")]
    add("S_OK_ALL",
        "F1 prefix_preserved is False and files == 2",
        p1["prefix_preserved"] is False and p1["files"] == 2,
        m1["prefix_preserved"] is False and m1["files"] == 2, "F1")

    # S_VACUOUS: empty tree must not report a preserved prefix
    p2, m2 = table[("F2", "pristine")], table[("F2", "S_VACUOUS")]
    add("S_VACUOUS",
        "F2 files == 0 and prefix_preserved is False",
        p2["files"] == 0 and p2["prefix_preserved"] is False,
        m2["files"] == 0 and m2["prefix_preserved"] is False, "F2")

    # S_RED_FILES: the selftest's own `red` must be False on a two-ledger tree
    p1b = table[("F1", "pristine")]
    add("S_RED_FILES",
        "F1 red is False (prefix_preserved False, files 2)",
        red_expr(False)(p1b) is False,
        red_expr(True)(p1b) is False, "F1")

    # negative control: the reverse-ordered pair does NOT discriminate S_OK_ALL
    neg = {"pristine": table[("F1b", "pristine")], "mutant": table[("F1b", "S_OK_ALL")]}
    neg_check = (neg["pristine"]["prefix_preserved"] is False
                 and neg["pristine"]["files"] == 2)
    neg_mutant = (neg["mutant"]["prefix_preserved"] is False
                  and neg["mutant"]["files"] == 2)
    print(f"\nNEGATIVE CONTROL F1b (edited ledger sorts last): pristine pp="
          f"{neg['pristine']['prefix_preserved']} mutant pp={neg['mutant']['prefix_preserved']}"
          f" -> proposed check {'would NOT kill' if neg_mutant else 'kills'} (fixture order is "
          f"part of the fix)")

    print("\nFIX TABLE  (proposed kake-backed selftest checks run on pristine vs survivor)")
    for c in checks:
        print(f"  {c['survivor']:<14} {c['fixture']} pristine={c['pristine']:<4} "
              f"mutant={c['mutant']:<4} {c['verdict']:<10} | {c['check']}")

    print("\nJSON")
    print(json.dumps({"pin": {"rev": a.rev, "path": PIN_PATH, "sha256": sha(blob)},
                      "recorded_mutant_hashes_equal": True,
                      "control": ctl, "fixtures": {k: {"root": str(v[0]), "rev": v[1]}
                                                   for k, v in fixtures.items()},
                      "readings": {f"{k[0]}/{k[1]}": v for k, v in table.items()},
                      "negative_control_f1b": {"reading": neg, "check_on_pristine": neg_check,
                                                "check_on_mutant": neg_mutant},
                      "checks": checks}, indent=1, sort_keys=True))
    return 0 if all(c["verdict"] == "KILLED" for c in checks) else 1


if __name__ == "__main__":
    sys.exit(main())
