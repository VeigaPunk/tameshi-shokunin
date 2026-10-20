# Evidence probe 2: exit/availability/pipe boundary relevant to exact-bytes gate. Stdlib only.
import subprocess, os, tempfile, stat
def sh(s): return ["/bin/sh", "-c", s]
print("P1 text=True universal newline CRLF:",
      subprocess.run(sh("printf 'x\\r\\n'"), capture_output=True, text=True, stdin=subprocess.DEVNULL).stdout.encode())
print("P2 text=True CR-only:",
      subprocess.run(sh("printf 'x\\ry'"), capture_output=True, text=True, stdin=subprocess.DEVNULL).stdout.encode())
r = subprocess.run(sh("printf 'x'"), capture_output=True, text=True, errors="strict", stdin=subprocess.DEVNULL)
print("P3 text=True invalid UTF-8 (strict):", end=" ")
try:
    subprocess.run(sh("printf '\\377'"), capture_output=True, text=True, stdin=subprocess.DEVNULL); print("no error")
except UnicodeDecodeError as e: print("UnicodeDecodeError ->", e.reason)
print("P4 signal death returncode:", subprocess.run(sh("kill -9 $$"), capture_output=True, stdin=subprocess.DEVNULL).returncode,
      "| shell $? view:", subprocess.run(sh("sh -c 'kill -9 $$'; echo $?"), capture_output=True, stdin=subprocess.DEVNULL).stdout)
for label, argv in [("missing binary", ["/nonexistent/xyz"]),
                    ("PATH-missing name", ["no-such-cmd-xyz"]),
                    ("non-executable file", ["/tmp/bytesreview/noexec.txt"]),
                    ("directory as argv0", ["/tmp"])]:
    open("/tmp/bytesreview/noexec.txt","w").write("x\n"); os.chmod("/tmp/bytesreview/noexec.txt", 0o644)
    try:
        p = subprocess.run(argv, capture_output=True, stdin=subprocess.DEVNULL); print(f"P5 {label}: rc={p.returncode}")
    except Exception as e: print(f"P5 {label}: {type(e).__name__} errno={getattr(e,'errno',None)}")
# Child exit code 64/2 must not leak as gate exit: child-only semantics
print("P6 child exit 64 captured as data:", subprocess.run(sh("exit 64"), capture_output=True, stdin=subprocess.DEVNULL).returncode)
# stdin inheritance: with DEVNULL, cat yields b''
print("P7 cat with stdin=DEVNULL:", subprocess.run(["cat"], capture_output=True, stdin=subprocess.DEVNULL, timeout=5).stdout)
# large dual-stream output: sequential read deadlocks; communicate() does not
big = "python3 -c \"import sys; sys.stdout.buffer.write(b'o'*400000); sys.stderr.buffer.write(b'e'*400000)\""
p = subprocess.Popen(["/bin/sh","-c",big], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL)
try:
    out = p.stdout.read(); err = p.stderr.read(); p.wait(timeout=5); print("P8 sequential read: completed", len(out), len(err))
except subprocess.TimeoutExpired:
    p.kill(); print("P8 sequential read: DEADLOCK (timeout) -> use communicate() or temp files")
o, e = subprocess.Popen(["/bin/sh","-c",big], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL).communicate(timeout=10)
print("P9 communicate():", len(o), len(e), "bytes exact")
# bash ignores NUL bytes in variables: already shown; check argv path with NUL cannot be passed
try:
    subprocess.run(["/bin/echo", "a\0b"]); print("P10 NUL in argv: accepted")
except ValueError as e: print("P10 NUL in argv: ValueError", e)
# file write/read byte fidelity
d = tempfile.mkdtemp(dir="/tmp/bytesreview")
data = b"a\r\n\0\xff\n"
with open(f"{d}/stdout.1", "wb") as f: f.write(data)
with open(f"{d}/stdout.1", "rb") as f: print("P11 rb roundtrip equal:", f.read() == data)
with open(f"{d}/stdout.1", "r", encoding="utf-8", errors="surrogateescape", newline=None) as f: t = f.read()
print("P12 text-mode readback differs (newline translation / encoding):", t.encode("utf-8","surrogateescape") != data)
