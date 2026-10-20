# Evidence probe: exact-bytes comparison boundary. Stdlib only. No repo writes.
import subprocess, sys, os, tempfile

def run(argv):
    p = subprocess.run(argv, stdin=subprocess.DEVNULL, capture_output=True)
    return p.returncode, p.stdout, p.stderr

def bytes_verdict(a, b):
    return "MATCH" if a == b else "DIFFER"

def sh(script):
    return ["/bin/sh", "-c", script]

cases = [
 ("T1 trailing newline", sh("printf 'x\\n'"), sh("printf 'x'"), "DIFFER"),
 ("T2 CRLF vs LF", sh("printf 'x\\r\\n'"), sh("printf 'x\\n'"), "DIFFER"),
 ("T3 empty vs single newline", sh("true"), sh("echo"), "DIFFER"),
 ("T4 empty vs empty", sh("true"), sh("true"), "MATCH"),
 ("T5 trailing space", sh("printf 'a '"), sh("printf 'a'"), "DIFFER"),
 ("T6 NUL-only vs empty", sh("printf '\\0'"), sh("true"), "DIFFER"),
 ("T7 NUL vs no-NUL", sh("printf 'a\\0b'"), sh("printf 'ab'"), "DIFFER"),
 ("T8 NUL differs at tail", sh("printf 'a\\0b'"), sh("printf 'a\\0c'"), "DIFFER"),
 ("T9 invalid UTF-8 bytes", sh("printf '\\377'"), sh("printf '\\376'"), "DIFFER"),
 ("T10 stderr-only diff", sh("echo same; echo e1 >&2"), sh("echo same; echo e2 >&2"), "DIFFER(stderr)"),
 ("T11 stdout-only diff", sh("echo a; echo e >&2"), sh("echo b; echo e >&2"), "DIFFER(stdout)"),
 ("T12 stderr same, stdout same", sh("echo a; echo e >&2"), sh("echo a; echo e >&2"), "MATCH"),
 ("T13 stderr empty vs newline", sh("echo a"), sh("echo a; echo >&2"), "DIFFER(stderr)"),
]

fail = 0
for name, a, b, expect in cases:
    ra, oa, ea = run(a)
    rb, ob, eb = run(b)
    got_out = bytes_verdict(oa, ob)
    got_err = bytes_verdict(ea, eb)
    got_exit = "MATCH" if ra == rb else "DIFFER"
    if expect == "MATCH":
        ok = got_out == got_exit == got_err == "MATCH"
    elif expect == "DIFFER":
        ok = "DIFFER" in (got_out, got_err)
    elif expect == "DIFFER(stderr)":
        ok = got_out == "MATCH" and got_err == "DIFFER"
    elif expect == "DIFFER(stdout)":
        ok = got_out == "DIFFER" and got_err == "MATCH"
    fail += (not ok)
    print(f"{name}: stdout={got_out} stderr={got_err} exit={got_exit} "
          f"(out {oa!r} vs {ob!r}; err {ea!r} vs {eb!r}) expect={expect} -> {'OK' if ok else 'UNEXPECTED'}")

# Trap probes: what naive comparisons would say for the same pairs.
print("\n# naive-comparison traps (must NOT be used by the gate)")
def naive_bash(a, b):
    x = subprocess.run(a, capture_output=True, stdin=subprocess.DEVNULL, text=True).stdout
    y = subprocess.run(b, capture_output=True, stdin=subprocess.DEVNULL, text=True).stdout
    return x == y
def naive_strip(a, b):
    x = run(a)[1].strip(); y = run(b)[1].strip(); return x == y
def naive_text_crlf(a, b):
    x = run(a)[1].decode(); y = run(b)[1].decode(); return x == y
def naive_bool(a, b):
    # treats empty output as "no output" and compares truthiness only
    x = run(a)[1]; y = run(b)[1]; return bool(x) == bool(y)
for name, a, b in [("T1", sh("printf 'x\\n'"), sh("printf 'x'")),
                   ("T2", sh("printf 'x\\r\\n'"), sh("printf 'x\\n'")),
                   ("T3", sh("true"), sh("echo")),
                   ("T6", sh("printf '\\0'"), sh("true")),
                   ("T7", sh("printf 'a\\0b'"), sh("printf 'ab'")),
                   ("T9", sh("printf '\\377'"), sh("printf '\\376'"))]:
    print(f"{name}: strip-eq={naive_strip(a,b)} text-mode-eq={naive_text_crlf(a,b) if name!='T9' else 'UnicodeDecodeError'} truthy-eq={naive_bool(a,b)}")
# bash command substitution (what shell-based gates would do)
import shlex
def bash_sub(script):
    return subprocess.run(["bash", "-c", f'printf "%s" "$({script})"'], capture_output=True).stdout
for name, s1, s2 in [("T1", "printf 'x\\n'", "printf 'x'"), ("T3", "true", "echo"),
                     ("T6", "printf '\\0'", "true"), ("T7", "printf 'a\\0b'", "printf 'ab'")]:
    print(f"{name}: bash-$(..)-eq={bash_sub(s1)==bash_sub(s2)} ({bash_sub(s1)!r} vs {bash_sub(s2)!r})")

print(f"\nPROBE_FAILURES={fail}")
