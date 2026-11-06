#!/usr/bin/env python3
"""Round-90 C2 fixes: append-only repairs of the round-89 closure's routed items 1-4.

Writes into TARGET (a lane checkout: the real lane at landing, a scratch clone in the
controls). Every edit is an append to an existing file, plus one row appended to
tools/registry.json's `rows` list, plus the registry-check receipt for that row run in
TARGET itself. Variants for controls: --variant wrongsection (README tokens under another
heading), --variant bogusregistry (row argv names a missing tool).

Usage: python3 -I fixes.py --target DIR [--variant pos|wrongsection|bogusregistry]
"""
import argparse, json, os, subprocess

README_HEAD = "## Round 90 — coverage-map repair (round-89 closure item 1)"
README = """
{head}

Appended; every earlier row is unchanged. Round 89 landed
`knowledge/kernel-witnessed-ledger.md` without a coverage-map row, so LEARNING's
`improved` test could not credit it (closure `lessons/round-89-verifier-spotcheck.md`
§4 and §6 item 1). This row places it.

| Entry | Map position and what it covers | Grounding |
|---|---|---|
| `knowledge/kernel-witnessed-ledger.md` | Frontier, not Core: the round-89 strace-witnessed audit of `tools/mutate-and-run.sh --regression` (`tools/ledger-witness.py`). R89-C1 was killed by its own rule (the T89E2 alias runners), so the entry records a killed instrument and its declared limits L1-L4; it moves no surface into Core | S313, S314 (mined, opened 2026-11-06); `.ufo/evidence/round-89/` |
"""

ENTRY = """
## Coverage-map row (appended round 90)

Appended; the entry above is unchanged. Its coverage-map row is
`corpus/README.md` § "Round 90 — coverage-map repair (round-89 closure item 1)":
Frontier, not Core, because R89-C1 was killed by its own rule (round-89 closure
§2.3). The row cites the same mined sources as this entry, S313 and S314.
"""

LESSON = """
## Round-90 corrections (append-only)

The text above is not rewritten; these corrections answer the round-89 closure's
routed items 2 and 3 (`round-89-verifier-spotcheck.md` §6).

1. `## Trend` says "the kill and four other mistakes". The `## Mistakes` table holds
   M1-M10: the kill (M6) and nine others. Corrected reading: the kill and nine other mistakes
   became lessons; QUALITY 136-138 are the grounded criteria among them.
2. The `## Gate` row rejecting mkcheck2 gives the reason "paywalled". It was not shown to
   be a paywall: at closure the ACM page and its PDF answered HTTP 403 behind a bot
   challenge, and no open manuscript was found. Corrected reason: the paper text was not retrievable at fetch time,
   so no quote could be located. The decision
   (reject) and its flip condition (an open manuscript with a located quote) are unchanged.
"""

SKILL = """
## Gate registry — round 90 (retained instrument: ledger witness)

Appended; earlier registry tables are unchanged. `tools/ledger-witness.py` (round 89) is a
retained instrument that had no registry row (round-89 closure §6 item 4, the R-4 class).
Its capability is **not admitted**: R89-C1 was killed by its own rule (T89E2 alias runners).
The row records how to run it and what it cannot see; it certifies nothing.

| Name | Kind | Entry command | Verdict map | Self-test command | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| ledger witness (not admitted) | probe | `python3 -I tools/ledger-witness.py --audit --runner RUNNER --fleet FLEET --trace TRACE --workdir WORKDIR --stdout STDOUT --rc RC` over an strace record of `tools/mutate-and-run.sh --regression` | `LEDGER_WITNESS: legs=N witnessed=N findings=0 checks=- PASS` exit 0; findings exit 1; setup exit 2 | `python3 -I tools/ledger-witness.py --selftest` → `LEDGER_WITNESS_SELFTEST: 21/21 pass` (registry row `ledger-witness-selftest`) | declared limits L1-L4 and the M6 alias class (hard link, directory swap, symlink) in `corpus/knowledge/kernel-witnessed-ledger.md` | TMPDIR scratch only | tameshi |
"""

ROW = {
    "name": "ledger-witness-selftest",
    "kind": "selftest",
    "argv": ["python3", "-I", "tools/ledger-witness.py", "--selftest"],
    "expect": {"exit": 0, "stdout_contains": ["LEDGER_WITNESS_SELFTEST: 21/21 pass"]},
    "timeout_s": 120,
    "source": "tools/ledger-witness.py@ff7a4b06:1-60",
    "status": "active",
    "tags": ["round-90", "not-admitted"],
}


def append(path, text):
    with open(path, "a", encoding="utf-8") as f:
        f.write(text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", required=True)
    ap.add_argument("--variant", default="pos", choices=["pos", "wrongsection", "bogusregistry"])
    a = ap.parse_args()
    t = os.path.realpath(a.target)
    head = README_HEAD if a.variant != "wrongsection" else "## Round 90 — misc notes"
    append(os.path.join(t, "corpus/README.md"), README.format(head=head))
    append(os.path.join(t, "corpus/knowledge/kernel-witnessed-ledger.md"), ENTRY)
    append(os.path.join(t, "corpus/lessons/round-89.md"), LESSON)
    append(os.path.join(t, "SKILL.md"), SKILL)
    rp = os.path.join(t, "tools/registry.json")
    reg = json.load(open(rp, encoding="utf-8"))
    row = dict(ROW)
    if a.variant == "bogusregistry":
        row["argv"] = ["python3", "-I", "tools/ledger-witness-missing.py", "--selftest"]
    reg["rows"].append(row)
    with open(rp, "w", encoding="utf-8") as f:
        f.write(json.dumps(reg, indent=1, ensure_ascii=True) + "\n")
    env = dict(os.environ)
    p = subprocess.run(["python3", "-I", "tools/registry-check.py", "--root", ".", "--only",
                        "ledger-witness-selftest"], cwd=t, capture_output=True, text=True, env=env)
    os.makedirs(os.path.join(t, ".ufo/evidence/round-90/c2"), exist_ok=True)
    with open(os.path.join(t, ".ufo/evidence/round-90/c2/registry-check-ledger-witness.txt"), "w") as f:
        f.write("$ python3 -I tools/registry-check.py --root . --only ledger-witness-selftest\n")
        f.write(p.stdout)
        f.write("exit=%d\n" % p.returncode)
    q = subprocess.run(["python3", "-I", "tools/ledger-witness.py", "--selftest"], cwd=t,
                       capture_output=True, text=True, env=env)
    with open(os.path.join(t, ".ufo/evidence/round-90/c2/ledger-witness-selftest.txt"), "w") as f:
        f.write("$ python3 -I tools/ledger-witness.py --selftest\n")
        f.write(q.stdout)
        f.write("exit=%d\n" % q.returncode)
    print("fixes written variant=%s registry_exit=%d selftest_exit=%d" % (a.variant, p.returncode, q.returncode))


if __name__ == "__main__":
    main()
