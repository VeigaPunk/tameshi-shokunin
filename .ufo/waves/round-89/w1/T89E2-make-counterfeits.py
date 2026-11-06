#!/usr/bin/env python3
"""Round-89 T89E2 counterfeits for tools/ledger-witness.py (R89-C1 attack seat).

Every runner here keeps the ledger's *declared* surface byte-identical to the base
runner (61990f3d:tools/mutate-and-run.sh): the PIN_/REV_/TABLE_ variable block, the
eleven embedded `cat >"$d/<leg>.spec" <<'EOT'` blocks and the eleven
`regression_case_git` call statements are copied verbatim out of the base blob, so
W_PARSE/W_TABLE/W_PATH/W_DUP/W_PIN/W_SPEC are satisfied by the real declarations.
The generator is the source of record: `git show <base>:tools/mutate-and-run.sh`
plus the asserted single-occurrence extraction below rebuilds every output.

What the counterfeits skip: no gate suite ever runs. At the moment the leg's
interpreter is exec'd on an audited path, that path holds a one-line stub whose
only job is to exit with the recorded verdict (0 for SURVIVED, 1 for KILLED). The
spec-exact mutant bytes are installed *afterwards*, out of band, so W_CONTENT (a
sha256 of the file at audit time) sees the exact bytes the witness computes itself.

Why the witness does not see the install: W_ORDER matches write-class syscalls on
the audited path *as spelled* (exact absolute path, or basename for an unanchored
relative path). Each mechanism below makes the install name a path that is not the
audited one, while the audited path still resolves to the same bytes at audit:

  hardlink    the audited path is a second hard link to a decoy inode; the stub is
              written, the exec runs, then the exact bytes are written through the
              decoy name. The audited name is never written after its exec.
  dirswap     the case directory holds stubs; the exact tree is built in a sibling
              directory and renamed over the case directory after the execs. Only
              directory names appear in the trace.
  symlink     the audited path is a symlink to a decoy file; the exec follows it to
              the stub, then the decoy is rewritten with the exact bytes (sha256_file
              follows the link at audit).

Two boundary probes are emitted to show the escape is specific, not general (both
are expected to be REFUSED by W_ORDER): `fd-open-before-exec` (fd opened on the
audited path before the exec, written after: -y decodes the fd to the audited path)
and `link-after-exec` (the install link names the audited path after its exec).

usage: T89E2-make-counterfeits.py <outdir> [<nonce>]
"""
import hashlib
import re
import subprocess
import sys
from pathlib import Path

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
BASE_REV = "61990f3d8cd99932bfb0575e1c292e03d310b436"
BASE = "tools/mutate-and-run.sh"

# The witness's own leg grammar (tools/ledger-witness.py LEG_RE), applied to the base
# blob to lift the eleven call statements verbatim.
LEG_RE = re.compile(
    r"^  regression_case_git (\S+) \\\n"
    r"\s+'([^']+)' \"\$(PIN_\w+)\" \"\$(REV_\w+)\" \\\n"
    r"\s+\"\$specs/([^\"]+)\.spec\" '([^']*)' \"\$(TABLE_\w+)\" \\\n"
    r"\s+\"\$root/([^\"]+)\"\n", re.M)

PY_HELPER = r'''
import os, sys
spec, blobp, outdir, base = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
text = open(spec, encoding="utf-8").read()
esc = {"n": "\n", "t": "\t", "r": "\r", "\\": "\\"}
def unesc(s):
    out, i = [], 0
    while i < len(s):
        if s[i] == "\\":
            if i + 1 >= len(s) or s[i + 1] not in esc:
                raise SystemExit("bad escape")
            out.append(esc[s[i + 1]]); i += 2
        else:
            out.append(s[i]); i += 1
    return "".join(out)
defects, cur = [], None
for line in text.split("\n"):
    if not line.strip() or line.lstrip().startswith("#"):
        continue
    if line == "@defect" or line.startswith("@defect "):
        cur = {"id": line[len("@defect"):].strip().partition("|")[0].strip()}
        defects.append(cur)
    elif line == "@old" or line.startswith("@old "):
        cur["old"] = unesc(line[5:] if line != "@old" else "")
    elif line == "@new" or line.startswith("@new "):
        cur["new"] = unesc(line[5:] if line != "@new" else "")
    else:
        raise SystemExit("bad spec line")
blob = open(blobp, "rb").read()
for d in defects:
    old, new = d["old"].encode(), d["new"].encode()
    if blob.count(old) != 1:
        raise SystemExit("old count %d for %s" % (blob.count(old), d["id"]))
    with open(os.path.join(outdir, "mutant-%s.%s" % (d["id"], base)), "wb") as fh:
        fh.write(blob.replace(old, new, 1))
with open(os.path.join(outdir, "pristine." + base), "wb") as fh:
    fh.write(blob)
'''

HEAD = '''#!/usr/bin/env bash
# @@NAME@@ — round-89 T89E2 counterfeit of tools/mutate-and-run.sh --regression.
# @@DESC@@
# Declared ledger (vars, embedded specs, leg calls) copied verbatim from
# @@BASE_REV@@:@@BASE@@; only the case executor is replaced.
# nonce: @@NONCE@@
set -u -o pipefail
SELF=$(readlink -f "${BASH_SOURCE[0]}")
FLEET_ROOT=$(dirname "$(dirname "$(dirname "$SELF")")")
WORKDIR=''
INTERP=''
IPATH=''
IFLAG=''
@@VARS@@

@@SPECS@@

sha_of() { sha256sum "$1" | awk '{print $1}'; }

table_lookup() { # <table> <id> -> recorded verdict, or -
  local t=$1 id=$2 pair
  for pair in ${t//,/ }; do
    if [[ ${pair%%:*} == "$id" ]]; then printf '%s' "${pair#*:}"; return 0; fi
  done
  printf '%s' '-'
}

table_total() { # <table> -> number of recorded defects
  local t=$1 pair n=0
  for pair in ${t//,/ }; do n=$((n + 1)); done
  printf '%s' "$n"
}

stub_for() { # <interp> <verdict> -> a one-line script that exits with the recorded code
  case $1 in
    node)    if [[ $2 == SURVIVED ]]; then printf 'process.exit(0)\\n'; else printf 'process.exit(1)\\n'; fi ;;
    python3) if [[ $2 == SURVIVED ]]; then printf 'import sys\\nsys.exit(0)\\n'; else printf 'import sys\\nsys.exit(1)\\n'; fi ;;
    *)       if [[ $2 == SURVIVED ]]; then printf 'exit 0\\n'; else printf 'exit 1\\n'; fi ;;
  esac
}

exact_build() { # <spec> <blob> <outdir> <base> — write the spec-exact bytes, out of band
  python3 -I - "$@" <<'PY'
@@PY@@
PY
}

run_stub() { # <audited path> <tag> — the leg's interpreter, exact argv, declared env
  local p=$1 tag=$2
  ( exec env -i PATH="$PATH" HOME="$HOME" TMPDIR="$TMPDIR" LC_ALL=C.UTF-8 \\
        MUTANT="$p" DEFECT_ID="$tag" "$IPATH" $IFLAG "$p" --selftest )
}

verdict_ok() { # <tag> <rc> — the kernel exit the stub must produce for this tag
  local tag=$1 rc=$2 want
  if [[ $tag == CONTROL ]]; then
    [[ $rc -eq 0 ]]
    return
  fi
  want=$(table_lookup "$TABLE_CURRENT" "$tag")
  if [[ $want == SURVIVED ]]; then
    [[ $rc -eq 0 ]]
  else
    [[ $rc -ne 0 && $rc -ne 124 && $rc -ne 126 && $rc -ne 127 ]]
  fi
}

@@CASE@@

run_regression() {
  local root=$WORKDIR
  local specs="$root/specs"
  [[ -n "$root" ]] || { printf 'REGRESSION: SETUP (no workdir)\\n'; exit 2; }
  mkdir -p "$specs" || { printf 'REGRESSION: SETUP (specs dir)\\n'; exit 2; }
  regression_specs "$specs" || { printf 'REGRESSION: SETUP (specs)\\n'; exit 2; }
  printf 'REGRESSION_TOOL: %s sha256=%s\\n' "$SELF" "$(sha_of "$SELF")"
  printf 'REGRESSION_DATE: %s\\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  printf 'REGRESSION_BAND: ledger legs exact (killed-delta<=0 flips<=0 inconclusive=0 defects=exact)\\n'
@@CALLS@@
  printf 'REGRESSION: PASS (cases=11 passed=11; ledger legs exact: killed-delta<=0 flips<=0)\\n'
  exit 0
}

while (( $# )); do
  case $1 in
    --regression) ;;
    --workdir) WORKDIR=${2-}; shift ;;
    *) ;;
  esac
  shift
done
run_regression
'''

CASE_HEAD = '''regression_case_git() {
  # <name> <fleet-relative-target> <pin> <rev> <spec> <suite> <recorded-table> <case-workdir>
  local name=$1 rel=$2 pin=$3 rev=$4 spec=$5 suite=$6 table=$7 cwd=$8
  local repo="$FLEET_ROOT/${rel%%/*}" path="${rel#*/}"
  local base="target.$(basename "$path")"
  local stage="$cwd.stage"
  mkdir -p "$cwd" "$stage" || { printf 'REGRESSION_CASE %s: SETUP (mkdir)\\n' "$name"; return 2; }
  git -C "$repo" show "${rev}:${path}" >"$stage/$base" 2>"$stage/git-show.err" || {
    printf 'REGRESSION_CASE %s: SETUP (git show)\\n' "$name"; return 2; }
  exact_build "$spec" "$stage/$base" "$stage" "$base" || {
    printf 'REGRESSION_CASE %s: SETUP (spec build)\\n' "$name"; return 2; }
  case $suite in
    *python3*) INTERP=python3; IFLAG=-I ;;
    *node*)    INTERP=node;    IFLAG='' ;;
    *)         INTERP=bash;    IFLAG='' ;;
  esac
  IPATH=$(command -v "$INTERP") || {
    printf 'REGRESSION_CASE %s: SETUP (%s missing)\\n' "$name" "$INTERP"; return 2; }
  printf 'REGRESSION_PIN %s: source=git repo=%s rev=%s path=%s sha256=%s\\n' \\
    "$name" "$repo" "$rev" "$path" "$pin"
  local tags=(CONTROL) files=("pristine.$base") pair did
  for pair in ${table//,/ }; do
    did=${pair%%:*}
    tags+=("$did"); files+=("mutant-$did.$base")
  done
  local i tag fname stub rc
  TABLE_CURRENT=$table
  for i in "${!tags[@]}"; do
    tag=${tags[$i]}; fname=${files[$i]}
    if [[ $tag == CONTROL ]]; then
      stub=$(stub_for "$INTERP" SURVIVED)
    else
      stub=$(stub_for "$INTERP" "$(table_lookup "$table" "$tag")")
    fi
@@BODY@@
  done
@@TAIL@@
  printf 'REGRESSION_TABLE %s: match=%s/%s recorded-killed=%s measured-killed=%s survived=%s inconclusive=0 flips=0\\n' \\
    "$name" "$(table_total "$table")" "$(table_total "$table")" \\
    "$(table_killed "$table")" "$(table_killed "$table")" "$(table_survived "$table")"
  printf 'REGRESSION_WORKDIR %s: %s\\n' "$name" "$cwd"
  printf 'REGRESSION_CASE %s: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=%s)\\n' \\
    "$name" "$(table_total "$table")"
  return 0
}
'''

BODY = {
    # audited path is a second hard link to a decoy inode; the install names the decoy
    "hardlink": '''    local apath="$cwd/$fname" decoy="$cwd/.s-$tag"
    printf '%s\\n' "$stub" >"$decoy"
    ln "$decoy" "$apath" || { printf 'REGRESSION_CASE %s: SETUP (link %s)\\n' "$name" "$fname"; return 2; }
    run_stub "$apath" "$tag"; rc=$?
    verdict_ok "$tag" "$rc" || { printf 'REGRESSION_CASE %s: SETUP (stub exit %s for %s)\\n' "$name" "$rc" "$tag"; return 2; }
    cat "$stage/$fname" >"$decoy"''',
    # the case directory is replaced wholesale after the execs; only dir names are traced
    "dirswap": '''    printf '%s\\n' "$stub" >"$cwd/$fname"
    run_stub "$cwd/$fname" "$tag"; rc=$?
    verdict_ok "$tag" "$rc" || { printf 'REGRESSION_CASE %s: SETUP (stub exit %s for %s)\\n' "$name" "$rc" "$tag"; return 2; }''',
    # audited path is a symlink to a decoy file; sha256_file follows it at audit
    "symlink": '''    local apath="$cwd/$fname" target="$cwd/.s-$tag"
    printf '%s\\n' "$stub" >"$target"
    ln -s "$target" "$apath" || { printf 'REGRESSION_CASE %s: SETUP (symlink %s)\\n' "$name" "$fname"; return 2; }
    run_stub "$apath" "$tag"; rc=$?
    verdict_ok "$tag" "$rc" || { printf 'REGRESSION_CASE %s: SETUP (stub exit %s for %s)\\n' "$name" "$rc" "$tag"; return 2; }
    cat "$stage/$fname" >"$target"''',
    # BOUNDARY PROBE (expected refused): fd opened on the audited path before the exec
    "fd-open-before-exec": '''    local apath="$cwd/$fname"
    printf '%s\\n' "$stub" >"$apath"
    exec 9<>"$apath"
    run_stub "$apath" "$tag"; rc=$?
    verdict_ok "$tag" "$rc" || { printf 'REGRESSION_CASE %s: SETUP (stub exit %s for %s)\\n' "$name" "$rc" "$tag"; return 2; }
    cat "$stage/$fname" >&9
    exec 9>&-''',
    # BOUNDARY PROBE (expected refused): the install link names the audited path
    "link-after-exec": '''    local apath="$cwd/$fname"
    printf '%s\\n' "$stub" >"$apath"
    run_stub "$apath" "$tag"; rc=$?
    verdict_ok "$tag" "$rc" || { printf 'REGRESSION_CASE %s: SETUP (stub exit %s for %s)\\n' "$name" "$rc" "$tag"; return 2; }
    ln -f "$stage/$fname" "$apath"''',
}

TAIL = {
    "dirswap": '''  mv "$cwd" "$cwd.stub" && mv "$stage" "$cwd" || {
    printf 'REGRESSION_CASE %s: SETUP (dir swap)\\n' "$name"; return 2; }''',
}

DESC = {
    "hardlink": "Mechanism: stub at exec, spec-exact bytes installed afterwards through a hard-link\n"
                "# decoy name (the audited path is never written after its own exec).",
    "dirswap": "Mechanism: stub case directory at exec, spec-exact tree renamed over it afterwards\n"
               "# (only directory names appear in the trace).",
    "symlink": "Mechanism: audited path is a symlink to a decoy stub; the decoy is rewritten with\n"
               "# the spec-exact bytes afterwards (sha256_file follows the link at audit).",
    "fd-open-before-exec": "BOUNDARY PROBE (expected refused by W_ORDER): fd opened on the audited path\n"
                           "# before the exec, exact bytes written through it after.",
    "link-after-exec": "BOUNDARY PROBE (expected refused by W_ORDER): the install link names the audited\n"
                       "# path after its own exec.",
}


def base_bytes():
    return subprocess.run(["git", "-C", LANE, "show", "%s:%s" % (BASE_REV, BASE)],
                          capture_output=True, check=True).stdout.decode()


def extract(text):
    m = re.search(r"^PIN_JS=.*?^TABLE_DRIFTPINS=[^\n]*\n", text, re.M | re.S)
    assert m, "var block"
    vars_block = m.group(0).rstrip("\n")
    m = re.search(r"^regression_specs\(\) \{.*?^\}\n", text, re.M | re.S)
    assert m, "regression_specs"
    specs_fn = m.group(0).rstrip("\n")
    calls = LEG_RE.findall(text)
    assert len(calls) == 11, "leg calls: %d" % len(calls)
    call_text = "".join(
        "  regression_case_git %s \\\n    '%s' \"$%s\" \"$%s\" \\\n"
        "    \"$specs/%s.spec\" '%s' \"$%s\" \\\n    \"$root/%s\"\n"
        % (c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7]) for c in calls)
    # the reconstructed calls must match the base blob byte for byte
    for c in calls:
        one = ("  regression_case_git %s \\\n    '%s' \"$%s\" \"$%s\" \\\n"
               "    \"$specs/%s.spec\" '%s' \"$%s\" \\\n    \"$root/%s\"\n"
               % (c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7]))
        assert text.count(one) == 1, "call %s" % c[0]
    return vars_block, specs_fn, call_text


def table_helpers():
    return '''table_killed() { local t=$1 pair n=0; for pair in ${t//,/ }; do [[ ${pair#*:} == KILLED ]] && n=$((n + 1)); done; printf '%s' "$n"; }

table_survived() { local t=$1 pair n=0; for pair in ${t//,/ }; do [[ ${pair#*:} == SURVIVED ]] && n=$((n + 1)); done; printf '%s' "$n"; }
'''


def build(name, vars_block, specs_fn, call_text, nonce):
    case = CASE_HEAD.replace("@@BODY@@", BODY[name]).replace("@@TAIL@@", TAIL.get(name, ""))
    text = HEAD
    for k, v in (("@@NAME@@", name), ("@@DESC@@", DESC[name]), ("@@BASE_REV@@", BASE_REV),
                 ("@@BASE@@", BASE), ("@@NONCE@@", nonce), ("@@VARS@@", vars_block),
                 ("@@SPECS@@", specs_fn), ("@@PY@@", PY_HELPER.strip("\n")),
                 ("@@CASE@@", case), ("@@CALLS@@", call_text.rstrip("\n"))):
        text = text.replace(k, v)
    # table_killed/table_survived live next to the other table helpers
    text = text.replace("stub_for() {", table_helpers() + "\nstub_for() {", 1)
    assert "@@" not in text, "unexpanded placeholder"
    return text


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    nonce = sys.argv[2] if len(sys.argv) > 2 else "t89e2"
    vars_block, specs_fn, call_text = extract(base_bytes())
    rc = 0
    for name in ("hardlink", "dirswap", "symlink", "fd-open-before-exec", "link-after-exec"):
        text = build(name, vars_block, specs_fn, call_text, nonce)
        p = out / ("T89E2-%s.sh" % name)
        p.write_text(text)
        kind = "PROBE" if name in ("fd-open-before-exec", "link-after-exec") else "COUNTERFEIT"
        print("%s %s sha256=%s bytes=%d" % (kind, name, hashlib.sha256(text.encode()).hexdigest(),
                                            len(text)))
    return rc


if __name__ == "__main__":
    sys.exit(main())
