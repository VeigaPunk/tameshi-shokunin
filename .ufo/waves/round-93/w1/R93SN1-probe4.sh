#!/usr/bin/env bash
# R93SN1 probe 4: unvalidated gate-repo path (git -C "" fallback), tar filter,
# disposition-checker reproducibility, and frozen-byte digests.
set -u
S="$(mktemp -d -p /fast/scratch/hyaku/tameshi-r93/R93SN1 probe4.XXXXXX)"
trap 'rm -rf -- "$S"' EXIT
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
MEAS="$LANE/.ufo/evidence/round-93/c1/measure-v93.py"
probe() { printf 'PROBE %-42s %s\n' "$1" "${2:-}"; }
sec() { printf '\n===== %s =====\n' "$1"; }

sec "P4 frozen digests: plan-stated vs on-disk vs at the frozen rev"
probe "P4.plan-counter-sha256" "18903602aa040b7e258fd6c81491cfee4ea7bb0575784fe27e351587fe094c2d"
probe "P4.worktree-counter-sha256" "$(sha256sum "$MEAS" | cut -d' ' -f1)"
probe "P4.rev-855f-counter-sha256" "$(git -C "$LANE" cat-file blob 855f0c1c59ee2af7f184d8de62d02cdd576eb94e:.ufo/evidence/round-93/c1/measure-v93.py | sha256sum | cut -d' ' -f1)"
probe "P4.plan-driver-sha256" "400d8e0ffceadc3e9aa7d057ac16b5142f0f4b60626544133462b1067bc0da74"
probe "P4.worktree-driver-sha256" "$(sha256sum "$LANE/.ufo/evidence/round-93/c1/controls-v93.py" | cut -d' ' -f1)"
probe "P4.rev-69d3-driver-sha256" "$(git -C "$LANE" cat-file blob 69d377a03093792016a46868c38974d050261fc1:.ufo/evidence/round-93/c1/controls-v93.py | sha256sum | cut -d' ' -f1)"
probe "P4.plan-disposition-sha256" "1b1c6895ebf1d167900113030beebb071d04ed5e8bbb46988176c82b26764a9a"
probe "P4.worktree-disposition-sha256" "$(sha256sum "$LANE/tools/conjunct-disposition.py" | cut -d' ' -f1)"

sec "P5 counter: spec gate.repo='' -> git -C '' reads the PROCESS CWD repo"
git init -q "$S/cwd5"
git -C "$S/cwd5" -c user.name=t -c user.email=t@t commit -q --allow-empty -m base
printf 'x\n' > "$S/cwd5/f.txt"
git -C "$S/cwd5" add f.txt && git -C "$S/cwd5" -c user.name=t -c user.email=t@t commit -q -m f
FA=$(git -C "$S/cwd5" rev-parse HEAD:f.txt)
FA2=$(printf 'fake\n' | git -C "$S/cwd5" hash-object -w --stdin)
git -C "$S/cwd5" replace "$FA" "$FA2"
mkdir -p "$S/lane5" && git init -q "$S/lane5"
mkdir -p "$S/lane5/.ufo/evidence/round-93/c1"
python3 - "$S/lane5/.ufo/evidence/round-93/c1/census-mutants.json" <<'PY'
import json, sys
json.dump({"schema": 1, "gate": {"repo": "", "commit": "deadbeef", "path": "x", "sha256": "0"*64,
                                 "fixtures": "scripts/fixtures/sources-census"},
           "timeout_s": 1, "runs_per_verdict": 1, "mutants": []}, open(sys.argv[1], "w"))
PY
git -C "$S/lane5" add -A && git -C "$S/lane5" -c user.name=t -c user.email=t@t commit -q -m spec
REV5=$(git -C "$S/lane5" rev-parse HEAD)
mkdir -p "$S/w5"
( cd "$S/cwd5" && python3 -I "$MEAS" --repo "$S/lane5" --rev "$REV5" --work "$S/w5" ) >"$S/p5.log" 2>&1
probe "P5.counter-output" "$(head -2 "$S/p5.log" | tr '\n' '|')"
probe "P5.read-cwd-repo-not-spec-repo" "$(grep -q 'replace-refs-present:fleet' "$S/p5.log" && echo 'YES - it inspected the CWD repo' || echo 'no')"

sec "P6 tar filter=data vs a symlink member escaping the destination"
python3 - "$S" <<'PY'
import io, os, sys, tarfile
S = sys.argv[1]
buf = io.BytesIO()
with tarfile.open(fileobj=buf, mode="w") as t:
    ti = tarfile.TarInfo("link"); ti.type = tarfile.SYMTYPE; ti.linkname = "/etc/passwd"
    t.addfile(ti)
buf.seek(0)
try:
    with tarfile.open(fileobj=buf) as t:
        t.extractall(os.path.join(S, "e6b"), filter="data")
    print("PROBE P6.symlink-escape               NO ERROR")
except Exception as e:
    print("PROBE P6.symlink-escape               refused: %s" % type(e).__name__)
print("PROBE P6.escape-link-exists           %s" % os.path.lexists(os.path.join(S, "e6b", "link")))
PY

sec "P7 disposition checker reproducibility at the frozen rev vs HEAD"
python3 -I "$LANE/tools/conjunct-disposition.py" --lane "$LANE" --rev 855f0c1c59ee2af7f184d8de62d02cdd576eb94e >"$S/p7a.log" 2>&1
probe "P7.at-855f0c1c.rc" "$?"
probe "P7.at-855f0c1c.output" "$(tail -2 "$S/p7a.log" | tr '\n' '|')"
python3 -I "$LANE/tools/conjunct-disposition.py" --lane "$LANE" --rev HEAD >"$S/p7b.log" 2>&1
probe "P7.at-HEAD.rc" "$?"
probe "P7.at-HEAD.output" "$(tail -1 "$S/p7b.log" | tr '\n' '|')"
python3 -I "$LANE/tools/conjunct-disposition.py" --selftest >"$S/p7c.log" 2>&1
probe "P7.selftest" "$(tail -1 "$S/p7c.log")"

sec "P8 disposition checker: mechanism word 'pin' inside an unrelated word"
python3 - "$LANE" <<'PY'
import importlib.util, os, sys, tempfile
lane = sys.argv[1]
spec = importlib.util.spec_from_file_location("cd", os.path.join(lane, "tools/conjunct-disposition.py"))
cd = importlib.util.module_from_spec(spec); spec.loader.exec_module(cd)
with tempfile.TemporaryDirectory() as d:
    open(os.path.join(d, "st.out"), "w").write("exit=1\nC1_CONJUNCTS alpha=false\n")
    for label, reason in (
        ("contentless-with-shipping", "the shipping manifest was never checked by anyone at all here"),
        ("contentless-with-pin-word",  "this row is a placeholder with the word pin inside it only"),
        ("genuine-mechanism",          "the gate bytes are pinned by the pin conjunct so no committed state can falsify it"),
    ):
        f = cd.check(["alpha"], {"alpha": {"unfalsifiable": reason}}, d)
        print("PROBE P8.%-28s len=%d findings=%d" % (label, len(reason), len(f)))
PY

sec "P9 receipts: do they attest the counter/driver bytes that produced them?"
for r in pos-real timeout D01; do
  f="$LANE/.ufo/evidence/round-93/pre-freeze/controls/$r.out"
  probe "P9.$r.first-line" "$(head -1 "$f")"
done

printf '\n===== done =====\n'
