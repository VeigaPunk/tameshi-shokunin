#!/usr/bin/env python3
"""T89M1 — build the witness defect spec from the pristine witness bytes.

Usage: python3 -I T89M1-make-spec.py <pristine-witness> <out.spec>

Every @old is a single-line substring of the pristine file asserted to occur
exactly once (so the spec is byte-exact by construction, not by retyping).
No backslashes in any snippet: the spec needs no escaping.
"""
import sys

# (id, old-substring, new-substring, description) — one probe per check W_PARSE..W_ENV
# (D01..D15, in CHECKS order), then eight sub-check / trace-parser probes (D16..D23).
DEFECTS = [
    ("D01_PARSE_UNRESOLVED",
     "if var not in vars_:",
     "if False:",
     "W_PARSE: an unresolved PIN_/REV_/TABLE_ variable is silently accepted"),
    ("D02_TABLE_INVERT",
     'if v not in ("KILLED", "SURVIVED")]',
     'if v in ("KILLED", "SURVIVED")]',
     "W_TABLE: recorded-verdict vocabulary check inverted (records every KILLED/SURVIVED, accepts anything else)"),
    ("D03_PATH_DOT",
     'return all(p not in ("", ".", "..") for p in parts)',
     'return all(p not in ("",) for p in parts)',
     'W_PATH: allows "." and ".." path components (dupbase-style leg spelling)'),
    ("D04_DUP_NO_PIN",
     '((l["name"], seen_name), (l["rel"], seen_rp), (l.get("pin"), seen_pin))',
     '((l["name"], seen_name), (l["rel"], seen_rp))',
     "W_DUP: blob-sha256 pin distinctness dropped (two legs may pin the same blob)"),
    ("D05_PIN_BLIND",
     'if sha256_bytes(blob) != l["pin"]:',
     "if False:",
     "W_PIN: declared PIN sha256 no longer compared to the blob"),
    ("D06_SPEC_COUNT",
     "if blob.count(old) != 1:",
     "if False:",
     "W_SPEC: old-string applicability (count==1) no longer enforced"),
    ("D07_RUN_SUMMARY",
     "if not summ or int(summ.group(1)) != len(legs) or int(summ.group(2)) != len(legs):",
     "if False:",
     "W_RUN: the REGRESSION summary line is never required"),
    ("D08_MAT_BLIND",
     'if not any(k == "exec" and os.path.basename(d[0]) == "git" and "show" in d[1] and want in d[1]',
     'if False and not any(k == "exec" and os.path.basename(d[0]) == "git" and "show" in d[1] and want in d[1]',
     "W_MAT: the per-leg `git show REV:PATH` exec is no longer required"),
    ("D09_CONTROL_EXIT",
     'if ex != ("code", 0):',
     "if False:",
     "W_CONTROL: the pristine control's exit status is no longer checked (never-exec branch untouched)"),
    ("D10_EXEC_ARGV",
     "return list(argv[1:]) == expect",
     "return target in list(argv[1:])",
     "W_EXEC: exact suite argv match weakened to `target anywhere in argv[1:]`"),
    ("D11_CONTENT_BLIND",
     "if got != exp:",
     "if False:",
     "W_CONTENT: mutant bytes no longer compared against the spec-applied blob"),
    ("D12_ORDER_BLIND",
     "if idx > exec_idx_by_path[q] and q not in reported:",
     "if False:",
     "W_ORDER: post-exec write-class syscalls on audited files no longer reported"),
    ("D13_VERDICT_BLIND",
     "if obs != rec:",
     "if False:",
     "W_VERDICT: kernel-observed verdict no longer compared to the table"),
    ("D14_EXTRA_BLIND",
     'if tgt not in expected_paths and not (case_dir in unaudited_cases and "/" in os.path.relpath(tgt, workdir)):',
     "if False:",
     "W_EXTRA: undeclared interpreter execs of mutant/pristine-shaped paths no longer reported"),
    ("D15_ENV_EQUALITY",
     'if did != "CONTROL" and cenv is not None and norm_env(exec_env.get(path), did, path) != cenv:',
     "if False:",
     "W_ENV: mutant exec environment no longer required to equal the leg control environment"),
    # ---- sub-check and trace-parser probes (not one-per-check) ----
    ("D16_ENV_DENY_NULL",
     'if kv.partition("=")[0] in ENV_DENY or kv.startswith("BASH_FUNC_")})',
     "if False})",
     "W_ENV sub-check: the steering-variable deny list (NODE_OPTIONS, BASH_ENV, LD_PRELOAD, BASH_FUNC_*) is never applied"),
    ("D17_RUN_PERLEG",
     "if sorted(passed) != sorted(set(names)) or len(passed) != len(names) or other:",
     "if other:",
     "W_RUN sub-check: per-leg PASS line count/set no longer compared to the legs (non-PASS lines still caught)"),
    ("D18_SPEC_IDS",
     'if [d for d, _, _ in spec] != [d for d, _ in l["table"]]:',
     "if False:",
     "W_SPEC sub-check: spec ids vs table ids equality no longer enforced"),
    ("D19_MAT_REV",
     'and "show" in d[1] and want in d[1]',
     'and "show" in d[1] and os.path.basename(path) in d[1]',
     "W_MAT sub-check: the exec must name REV:PATH, not merely PATH (a wrong-rev `git show` passes)"),
    ("D20_EXEC_TOKENIZER_UNESCAPE",
     "out = [c_unescape(m.group(1))]",
     "out = [m.group(1)]",
     "trace exec tokenizer: the exec filename is taken raw (no C-unescape), argv keeps unescaping"),
    ("D21_EXIT_SIGNAL_DROP",
     "if em:",
     "if em and em.group(2):",
     "trace exit parser: `+++ killed by SIG... +++` exits are dropped instead of recorded as ('signal', name)"),
    ("D22_WRITE_ANCHOR_REL",
     "hits = [q for q in exec_idx_by_path if os.path.basename(q) == b]",
     "hits = []",
     "trace write anchoring: an unanchored relative write path (REL:) matches nothing"),
    ("D23_UNFINISHED_DROP",
     'if body.endswith("<unfinished ...>"):',
     "if False:",
     "trace parser: `<unfinished ...>`/`<... resumed>` continuation buffering disabled"),
]


def main(argv):
    if len(argv) != 2:
        sys.stderr.write(__doc__)
        return 2
    src, out = argv
    with open(src, "rb") as fh:
        text = fh.read().decode("utf-8")
    lines = []
    for did, old, new, desc in DEFECTS:
        if old == new:
            sys.stderr.write("%s: no-op\n" % did)
            return 2
        if "\n" in old or "\n" in new or "\\" in old or "\\" in new:
            sys.stderr.write("%s: multiline or backslash snippet unsupported\n" % did)
            return 2
        n = text.count(old)
        if n != 1:
            sys.stderr.write("%s: old-count=%d expected 1: %r\n" % (did, n, old))
            return 2
        if "\t" in desc:
            sys.stderr.write("%s: tab in description\n" % did)
            return 2
        lines.append("@defect %s | %s\n@old %s\n@new %s\n" % (did, desc, old, new))
    body = ("# T89M1 witness defect spec — 23 single-edit defects against\n"
            "# tools/ledger-witness.py @ 8876cca5dbb877b168aa09a86128d672f6b4ed5a.\n"
            "# Generated by T89M1-make-spec.py from the pristine bytes; every @old is a\n"
            "# single-line substring asserted to occur exactly once (the runner re-asserts).\n"
            "# Suite: python3 -I \"$MUTANT\" --selftest  (the witness's own 21-fixture arms).\n" + "\n".join(lines))
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(body)
    for did, _, _, _ in DEFECTS:
        print(did)
    print("SPEC_DEFECTS: %d" % len(DEFECTS))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
